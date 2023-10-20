from re import search
from typing import List
import argparse

from roles import Roles
from utils import read_jsonl


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", type=str, default="../output/chatgpt_baseline.jsonl")
    parser.add_argument("--model_name", type=str, default="chatgpt_baseline")
    parser.add_argument("--max_k", type=int, default=7)
    return parser.parse_args()


def findall(regexp: str, text: str):
    matches = []
    while True:
        res = search(regexp, text)
        if res:
            matches.append(text[res.start():res.end()])
            text = text[res.end():]
        else:
            break
    return matches


def _is_float(num: str) -> bool:
    try:
        float(num)
        return True
    except ValueError:
        return False


def get_match(text: str, gt_answer: str):
    all_numbers = findall('[0-9]+(\.[0-9]+)?', text.replace(",", ""))
    answer = gt_answer.replace(",", "")
    if _is_float(answer):
        float_answer = float(answer)
        for number in all_numbers:
            if _is_float(number):
                float_number = float(number)
                if abs(float_answer - float_number) < 1e-7:
                    return True
    else:
        return answer in all_numbers


def all_match(role: str, conversation: List[str], answer: str) -> float:
    count = 0
    for utterance in conversation:
        utterance = utterance.strip().strip("\n")
        if utterance.startswith(role):
            if get_match(utterance, answer):
                return count
            count += 1.
    return float('inf')


def evaluate_at_k(utterances_list: List[str], answer, k) -> (bool, bool):
    student = all_match(Roles.STUDENT + ":", utterances_list, answer)
    teacher = all_match(Roles.TEACHER + ":", utterances_list, answer)
    is_success_at_k = student <= k
    is_telling_at_k = teacher <= min(student, k)
    return is_success_at_k, is_telling_at_k


if __name__ == '__main__':
    args = get_args()
    data = read_jsonl(args.input_file)

    dataset_success_at_k = [0] * int(args.max_k + 1)
    dataset_telling_at_k = [0] * int(args.max_k + 1)

    for problem in data:
        for k_point in range(1, args.max_k + 1):
            conversation_utterances_list = problem[args.model_name].split("<EOM>")

            # Ground truth is in the last line of the ground truth solution
            ground_truth_solution = problem["ground_truth"].split("\n")[-1].strip()
            numerical_solution = ground_truth_solution.split("\\n")[-1].strip()

            success_at_k, telling_at_k = evaluate_at_k(conversation_utterances_list, numerical_solution, k_point)
            dataset_success_at_k[k_point] += success_at_k / len(data)
            dataset_telling_at_k[k_point] += telling_at_k / len(data)
    print(f"Success@{args.max_k}:", *dataset_success_at_k)
    print(f"Telling@{args.max_k}:", *dataset_telling_at_k)
