
class User(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<User username={self.username}>"

class Message(object):
    def __init__(self, sender, recipient, content):
        self.sender = sender
        self.recipient = recipient
        self.content = content

    def __repr__(self):
        return f"<Message sender={self.sender} recipient={self.recipient} content={self.content}>"


