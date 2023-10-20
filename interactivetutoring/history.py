from typing import Dict

from message import Message


class History(object):
    def __init__(self):
        self.messages = []
        self.turns = 0

    def add_message(self, message: Message):
        self.messages.append(message)
        self.turns += 1

    def __str__(self):
        return "\n\n".join([str(message) for message in self.messages])

    def to_delimited_string(self, delimiter: str):
        return delimiter.join([str(message) for message in self.messages])

    def to_gpt_messages(self, role_mapping: Dict[str, str]):
        return [message.to_gpt_format(role_mapping) for message in self.messages]
