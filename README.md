# 🧮 MathDial: A Dialogue Tutoring Dataset with Rich Pedagogical Properties Grounded in Math Reasoning Problems
https://arxiv.org/abs/2305.14536

🧮 MathDial is grounded in math word problems as well as student confusions which provide a challenging testbed for creating faithful and equitable dialogue tutoring models able to reason over complex information. Current models achieve high accuracy in solving such problems but they fail in the task of teaching.
![overview](generations.png)

# Description
Although automatic dialogue tutors hold great potential in making education personalized and more accessible, research on such systems has been hampered by a lack of sufficiently large and high-quality datasets. However, collecting such datasets remains challenging, as recording tutoring sessions raises privacy concerns and crowdsourcing leads to insufficient data quality. To address this problem, we propose a framework to semi-synthetically generate such dialogues by pairing real teachers with a large language model (LLM) scaffolded to represent common student errors. In this paper, we describe our ongoing efforts to use this framework to collect 🧮 MathDial, a dataset of currently ca. 1.5k tutoring dialogues grounded in multi-step math word problems. We show that our dataset exhibits rich pedagogical properties, focusing on guiding students using sense-making ques- tions to let them explore problems. Moreover, we outline that 🧮 MathDial and its grounding annotations can be used to finetune language models to be more effective tutors (and not just solvers) and highlight remaining challenges that need to be addressed by the research community. We will release our dataset publicly to foster research in this socially important area of NLP.

Source of math problems: [GSM8k](https://github.com/openai/grade-school-math)

# Dataset
The dataset is available in the data folder. For full dataset see `data/mathdial.tsv` or `data/mathdial.jsonl` and for a small sample see `data/sample.jsonl`

## Data Structure
- `qid` - unique identifier of the problem
- `scenario` - order of the problem in the data collection, out of the 5 scenarios in a session
- `question` - math problem text
- `ground_truth` - correct answer to the problem
- `student_incorrect_solution` - student incorrect solution to the problem caused by some confusion
- `student_profile` - student profile based on general math problem solving student misconceptions
- `teacher_described_confusion` - teacher annotated student confusion in free text
- `self-correctness` - teacher annotated whether student solved the problem correctly by the end of the conversation
    - options: `Yes, Yes, but I had to reveal the answer, No`
- `self-typical-confusion` - teacher annotated whether student exhibited a typical 7th grade confusion, Likert scale 1 (unlikely) to 5 (very likely)
- `self-typical-interactions` - teacher annotated whether student exhibited typical 7th grade interactions, Likert scale 1 (unlikely) to 5 (very likely)
- `conversation` - conversation in a string format with `|EOM|` delimiter between Teacher and Student personas  `Persona: (dialog_act) text` e.g. `Teacher: (focus) What is the difference?|EOM|Student: I mean ...|EOM|Teacher:`


## HuggingFace Loader

# Setup your environment
```bash 
pip install -r requirements.txt
export OPENAI_API_KEY=<your-openai-api-key>
```

# Teacher model - Generate next tutor response
```bash
python interactivetutoring/gpt_baseline.py --input_file <dataset-path> --model_name <name-of-your-model> --max_utterances <stopping-point> --export_file <export-file-with-conversations>
```
Example using ChatGPT3.5 as a teacher model and small data sample:
```bash
python interactivetutoring/gpt_baseline.py --input_file data/sample.jsonl --model_name chatgpt_baseline --max_utterances 5 --export_file output/chatgpt_baseline.jsonl
```
Please see `interactivetutoring/teachers.py` how to add your own teacher model.

# Evaluate your teacher model using simulated student
```bash
python interactivetutoring/evaluate.py --input_file <path-to-file-with-generations> --model_name <model-name>  
```
Example using dummy data:
```bash
python interactivetutoring/evaluate.py --input_file output/example_model_output.jsonl --model_name chatgpt_baseline  
```


# Citation
Please cite the following:
> Macina*, J., Daheim*, N., Chowdhury*, S.P., Sinha, T., Kapur, M., Gurevych, I., Sachan, M. (2023) [🧮 MathDial: A Dialogue Tutoring Dataset with Rich Pedagogical Properties Grounded in Math Reasoning Problems](https://arxiv.org/abs/2305.14536). _arXiv preprint arXiv:2305.14536_

