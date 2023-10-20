from typing import Dict


class Message(object):
    def __init__(self, persona: str, text: str):
        self.persona = persona
        self.text = text.replace('\n', '\\n')

    def __str__(self):
        return f"{self.persona}: {self.text}"

    def to_gpt_format(self, role_mapping: Dict[str, str]):
        return {"role": role_mapping.get(self.persona, "unknown"), "content": self.text}
