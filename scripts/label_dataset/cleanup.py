import json


data = json.load(open("workex_result.json", "r"))
jds = json.load(open("../../data/cleaned/all_job_descriptions.json", "r"))
jds_by_key = {}
cleaned = {}
cleaned_list = []

for i in jds:
    jds_by_key[jds[i]["id"]] = jds[i]["description"]


for i in data:

    description = jds_by_key[i]

    for j in data[i]:
        curr_dict = {}
        curr_dict["job_description"] = description
        curr_dict["work_experience"] = j[0]
        curr_dict["label"] = j[1]
        curr_dict["feedback"] = j[2]
        cleaned_list.append(curr_dict)

cleaned["data"] = cleaned_list
json.dump(cleaned, open("formatted_workex.json", "w"), indent=2)


