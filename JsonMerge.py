import json

json_file_path = "output/output4.json"
wrapper_file_path = "output/output5.txt"
output = "output/output6.json"

with open(wrapper_file_path, "r", encoding="utf-8") as f:
    new_wrappers = json.load(f)
new_wrappers_dict = {wrapper["id"]: wrapper for wrapper in new_wrappers}

with open(json_file_path, "r", encoding="utf-8") as f:
    original_data = json.load(f)

def replace_wrappers(obj):
    if isinstance(obj, dict):
        if obj.get("type") == "wrapper" and "id" in obj and obj["id"] in new_wrappers_dict:
            return new_wrappers_dict[obj["id"]]
        return {key: replace_wrappers(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [replace_wrappers(item) for item in obj]
    return obj

updated_data = replace_wrappers(original_data)

with open(output, "w", encoding="utf-8") as f:
    json.dump(updated_data, f, indent=4, ensure_ascii=False)

print("Updated JSON saved as", output)
