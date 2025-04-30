import random

import requests
import json
import subprocess

def query_ollama(prompt):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "deepseek-r1:1.5b",
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(url, json=data)
    return response.json()["response"]


def run_ollama_cli(prompt):
    process = subprocess.Popen(
        ['ollama', 'run', 'deepseek-r1:1.5b'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,  # 👈 This is key
        encoding='utf-8'
    )

    stdout, stderr = process.communicate(input=prompt)
    return stdout


# for i in range(10):
#     output = run_ollama_cli("What is reinforcement learning?")
#     print(output)


def classify_output(text: str):
    positive = text.count("positive") + text.count("Positive")
    negative = text.count("negative") + text.count("Negative")
    return "positive" if positive > negative else "negative"

WORK_EX = open("../../data/resumes/work_experience/workex.txt", "r").read().split("\n\n")
job_des_data = json.load(open("../../data/cleaned/all_job_descriptions.json"))
result = json.load(open("result.json", "r"))
JOB_DES = random.sample([job_des_data[i] for i in job_des_data if (len(job_des_data[i]["id"]) < 20 and job_des_data[i]["id"] not in result)], 100)
index = 0

for i in JOB_DES:
    result[i["id"]] = []
    print(i["id"])
    for j in WORK_EX:
        print(index)
        curr_res = [j]
        curr_des = i["description"]
        output = run_ollama_cli(f"{curr_des} Classify positive if this job description matches this following Job experience else"
                                f" classify negative, be lenient in evaluation {j}")
        if output is not None:
            class_out = classify_output(output)
            curr_res.append(class_out)
            curr_res.append(output)
            print(class_out)
            result[i["id"]].append(curr_res)
            index+=1
    json.dump(result, open("result.json", "w"), indent=2)
