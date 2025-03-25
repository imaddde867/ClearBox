import uvicorn
import os
from dotenv import load_dotenv
import argparse

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the ClearBox API server")
    parser.add_argument("--port", type=int, default=int(os.getenv("PORT", 8000)), help="Port to run the server on")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to run the server on")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload for development")
    
    args = parser.parse_args()
    
    print(f"Starting ClearBox API server on {args.host}:{args.port}")
    
    uvicorn.run(
        "app.main:app",
        host=args.host,
        port=args.port,
        reload=args.reload
    ) 