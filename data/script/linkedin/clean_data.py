import json
import os

files = os.listdir("./data")
combined_list = []
for file in files:
    file_data = json.load(open(f"./data/{file}", "r"))
    for i in file_data:
        if file_data[i] is not None:
            file_data[i]["type"] = file.split(".")[0]
    combined_list += [file_data[i] for i in file_data if file_data[i] is not None]

combined_list_dict = {i:combined_list[i] for i in range(len(combined_list))}

json.dump(combined_list_dict, open("../../cleaned/all_job_descriptions.json", "w"), indent=2)
print(f"Combined {len(combined_list_dict)} Job Descriptions")
