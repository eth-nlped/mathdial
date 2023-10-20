import json
import time
import openai
from typing import List, Dict


def read_jsonl(path: str) -> List[Dict]:
    with open(path) as fh:
        return [json.loads(line) for line in fh.readlines() if line]


def call_chatgpt_api(messages: List[str], system_prompt: str, stop: List[str]):
    retries = 0
    while True:
        try:
            if retries > 0:
                print("sleeping for 1 second")
                time.sleep(1 + retries)
            retries += 1
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": system_prompt}, *messages],
                temperature=0,
                max_tokens=512,
                stop=stop,
            )
            return response
        except Exception as e:
            print("Chatgpt", e)
