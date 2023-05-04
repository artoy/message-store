import uuid


class Message:
    def __init__(self, channel_id, user, text, timestamp):
        self.id = str(uuid.uuid4())
        self.channel_id = channel_id
        self.user = user
        self.text = text
        self.timestamp = timestamp
