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

def extract_math_blocks_list(tex_file: str) -> list:
    try:
        with open(tex_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        return [f"Error reading math file {tex_file}: {e}"]

    blocks = []
    i = 0
    while i < len(lines):
        if lines[i].strip().lower().startswith("math block"):
            block_header = lines[i].strip()
            if i + 1 < len(lines):
                block_content = lines[i + 1].strip()
                blocks.append(f"{block_header}\n{block_content}")
            i += 2
        else:
            i += 1
    return blocks

def send_batch(prompt_text: str, csv_content: str, math_batch: list) -> str:
    blocks_text = "\n\n".join(math_batch)
    full_prompt = f"{prompt_text}\n\ndictionaries for my json:\n{csv_content}\n\nMath Blocks:\n{blocks_text}"
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": full_prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred during the API call: {e}"

def send_complete_prompt(txt_file: str, csv_file: str, tex_file: str) -> str:
    prompt_text = read_file(txt_file)
    csv_content = read_file(csv_file)
    math_blocks = extract_math_blocks_list(tex_file)

    all_responses = []
    for i in range(0, len(math_blocks), 2):
        batch = math_blocks[i:i+3]
        response = send_batch(prompt_text, csv_content, batch)
        all_responses.append(response)

    return "\n\n".join(all_responses)

if __name__ == "__main__":
    txt_file_path = "dict/prompt1.txt"
    csv_file_path = "dict/dict.csv"
    tex_file_path = "output/output3.tex"
    result = send_complete_prompt(txt_file_path, csv_file_path, tex_file_path)
    os.makedirs("output", exist_ok=True)
    with open("output/output5.txt", "w", encoding="utf-8") as f:
        f.write(result)

