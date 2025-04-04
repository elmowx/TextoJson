import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def read_file(file_path: str) -> str:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file {file_path}: {e}"

def send_complete_prompt(txt_file: str, json_file: str, wrapper_file: str) -> str:
    prompt_text = read_file(txt_file)
    json_content = read_file(json_file)
    wrapper_content = read_file(wrapper_file)
    full_prompt = f"{prompt_text}\n\nJson itself:\n{json_content}\n\n New wrappers:\n{wrapper_content}"
    try:
        response = client.chat.completions.create(model="o3-mini",
        messages=[{"role": "user", "content": full_prompt}])
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred during the API call: {e}"

if __name__ == "__main__":
    txt_file_path = "dict/prompt2.txt"
    json_file_path = "output/output4.json"
    wrapper_file_path = "output/output5.txt"
    result = send_complete_prompt(txt_file_path, json_file_path, wrapper_file_path)
    with open("output/output6.json", "w", encoding="utf-8") as f:
        f.write(result)
