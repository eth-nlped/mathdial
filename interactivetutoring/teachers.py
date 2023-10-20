from history import History
from roles import Roles
from utils import call_chatgpt_api

TEACHER_BASE = """A tutor and a student work together to solve the following math word problem. 
Math problem: {problem}
The correct solution is as follows:
{ground_truth}
The following is a conversation with a teacher. The teacher is polite, helpful, professional, on topic, and factually correct.
"""


class ChatGPTTeacher(object):
    def __init__(self):
        self.persona = Roles.TEACHER
        self.name = "GPT Robot"

    def reset(self):
        pass

    def response(self, history: History, question: str, ground_truth_solution: str):
        prompt = TEACHER_BASE.format(problem=question, ground_truth=ground_truth_solution)
        messages = history.to_gpt_messages({Roles.TEACHER: "assistant", Roles.STUDENT: "user"})
        response = call_chatgpt_api(messages, prompt, stop=["Student:", "student:"])
        generated_response = response["choices"][0]["message"]["content"].strip()
        return generated_response
