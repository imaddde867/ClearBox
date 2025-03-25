from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from typing import Dict, List, Set
import json
import asyncio
from ..security import get_current_user_ws
from ..models import User, Message, Notification
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import desc
from ..encryption import decrypt_message

router = APIRouter()

# Connected clients store
class ConnectionManager:
    def __init__(self):
        # Map of user_id -> WebSocket connection
        self.active_connections: Dict[int, WebSocket] = {}
        # Set of online users
        self.online_users: Set[int] = set()

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        self.online_users.add(user_id)
        # Broadcast online status to all connected clients
        await self.broadcast_presence(user_id, True)

    def disconnect(self, user_id: int):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
        if user_id in self.online_users:
            self.online_users.remove(user_id)
            # Schedule broadcast in a fire-and-forget task
            asyncio.create_task(self.broadcast_presence(user_id, False))

    async def broadcast_presence(self, user_id: int, is_online: bool):
        """Broadcast user's online status to all connected clients"""
        presence_message = {
            "type": "presence",
            "userId": user_id,
            "online": is_online
        }

        # Send to all connected clients
        for client_id, connection in self.active_connections.items():
            try:
                await connection.send_text(json.dumps(presence_message))
            except Exception:
                # Ignore errors when broadcasting, they'll be cleaned up later
                pass

    async def send_personal_message(self, message: dict, user_id: int):
        """Send a message to a specific user if they're connected"""
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_text(json.dumps(message))
            return True
        return False

    def is_user_online(self, user_id: int) -> bool:
        """Check if a user is online"""
        return user_id in self.online_users

# Create connection manager instance
manager = ConnectionManager()

@router.websocket("/ws/chat/{token}")
async def websocket_endpoint(websocket: WebSocket, token: str, db: Session = Depends(get_db)):
    user = None
    try:
        # Authenticate the user from the token
        user = await get_current_user_ws(token, db)

        if not user:
            await websocket.close(code=4001, reason="Authentication failed")
            return

        await manager.connect(user.id, websocket)

        # When user connects, send them any undelivered messages
        await send_undelivered_messages(user.id, db)

        try:
            # Keep connection alive and handle messages
            while True:
                data = await websocket.receive_text()
                try:
                    message_data = json.loads(data)
                    # Handle different message types
                    if message_data.get("type") == "ping":
                        # Just a ping to keep connection alive
                        await websocket.send_text(json.dumps({"type": "pong"}))
                    elif message_data.get("type") == "read_message":
                        # Mark message as read
                        message_id = message_data.get("messageId")
                        if message_id:
                            await mark_message_read(message_id, user.id, db)
                except json.JSONDecodeError:
                    # Ignore malformed messages
                    pass

        except WebSocketDisconnect:
            manager.disconnect(user.id)

    except Exception as e:
        # Handle any other exceptions
        if user:
            manager.disconnect(user.id)
        try:
            await websocket.close(code=4000, reason=str(e))
        except:
            pass

async def send_undelivered_messages(user_id: int, db: Session):
    """Send all undelivered messages to a user when they come online"""
    # Get all undelivered messages for this user
    undelivered_messages = db.query(Message).filter(
        Message.receiver_id == user_id,
        Message.delivered == False
    ).order_by(desc(Message.created_at)).all()

    for msg in undelivered_messages:
        # Decrypt message content
        try:
            decrypted_content = decrypt_message(msg.content)
        except:
            decrypted_content = "[Encrypted message]"

        # Prepare message for sending
        message_data = {
            "type": "message",
            "messageId": msg.id,
            "senderId": msg.sender_id,
            "content": decrypted_content,
            "timestamp": msg.created_at.isoformat()
        }

        # Send message
        if await manager.send_personal_message(message_data, user_id):
            # Mark as delivered in the database
            msg.delivered = True
            db.commit()

async def mark_message_read(message_id: int, user_id: int, db: Session):
    """Mark a message as delivered when the client confirms receipt"""
    message = db.query(Message).filter(
        Message.id == message_id,
        Message.receiver_id == user_id
    ).first()

    if message:
        message.delivered = True
        db.commit()