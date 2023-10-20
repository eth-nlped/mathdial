import openai
import time

from history import History
from roles import Roles

STUDENT_PROMPT = """
Student Persona: (STUDENT PERSONA)

Math problem: (MATH PROBLEM)

Student solution: (STUDENT SOLUTION)

Context: (STUDENT NAME) thinks their answer is correct. Only when the teacher provides several good reasoning questions, (STUDENT NAME) understands the problem and corrects the solution. (STUDENT NAME) can use calculator and thus makes no calculation errors. Send <EOM> tag at end of the student message.

(DIALOG HISTORY)

Student:
"""

STUDENT_NAME = "Kayla"
STUDENT_PERSONA = STUDENT_NAME + " is a 7th grade student. She has problem with understanding of what steps or procedures are required to solve a problem."


class InstructGPTStudent(object):
    def __init__(self):
        self.persona = Roles.STUDENT
        self.name = STUDENT_NAME

    def reset(self):
        pass

    def response(self, history: History, question: str, incorrect_solution: str):
        response = ""
        messages = history.to_delimited_string("<EOM>\n\n")
        prompt = STUDENT_PROMPT.replace("(STUDENT PERSONA)", STUDENT_PERSONA).replace("(STUDENT SOLUTION)",
                                                                                      incorrect_solution).replace(
            "(MATH PROBLEM)", question).replace("(STUDENT NAME)", STUDENT_NAME).replace(
            "(DIALOG HISTORY)", messages)
        errors_counter = 0
        done = False
        while not done:
            try:
                response = openai.Completion.create(
                    model="gpt-3.5-turbo-instruct",
                    prompt=prompt,
                    temperature=0,
                    max_tokens=512,
                    stop=["Teacher:", "teacher:"],
                )
                response = response["choices"][0]["text"].strip()
                done = True
            except Exception as e:
                print(e)
                errors_counter += 1
                time.sleep(1)
        utterance = response.replace("Student:", "").replace(STUDENT_NAME + ":", "").replace("<EOM>", "").strip(
            "\n")
        return utterance
