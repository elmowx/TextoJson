import json
import re
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

input_file = r"C:\Users\kecko\Documents\corc\output\output3.tex"
output_file = r"C:\Users\kecko\Documents\corc\output\output5.json"
constants_file = r"C:\Users\kecko\Documents\corc\dictionaries\constants.json"
functions_file = r"C:\Users\kecko\Documents\corc\dictionaries\functions.json"

def load_json_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def extract_math_blocks(file_path):
    math_blocks = []
    current_block = None
    current_type = None

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            math_match = re.match(r'^math block\s*\d+:', line, re.IGNORECASE)
            text_match = re.match(r'^text block\s*\d+:', line, re.IGNORECASE)
            
            if math_match:
                if current_block is not None and current_type == "math":
                    math_blocks.append(current_block.strip())
                current_type = "math"
                current_block = ""
            elif text_match:
                if current_block is not None and current_type == "math":
                    math_blocks.append(current_block.strip())
                current_type = "text"
                current_block = ""
            else:
                if current_block is not None:
                    current_block += line + " "
        if current_block is not None and current_type == "math":
            math_blocks.append(current_block.strip())
    return math_blocks

def convert_math_blocks_to_wrappers(math_blocks):
    constants_dict = load_json_file(CONSTANTS_FILE)
    functions_dict = load_json_file(FUNCTIONS_FILE)

    system_instructions = (
        "You are an assistant that converts LaTeX math blocks into a JSON structure of math wrappers. "
        "Follow these rules precisely: \n"
        "- Each math expression is to be wrapped in a 'wrapper' node with an 'inline' child node. \n"
        "- The conversion must use the constants and functions dictionaries provided. \n"
        "- Each wrapper must have a unique id in the format 'wrapperIdX', where X starts at 1. \n"
        "Return only a JSON list of wrapper nodes without any extra text."
    )

    user_instructions = (
        f"Constants dictionary:\n{json.dumps(constants_dict, indent=2)}\n\n"
        f"Functions dictionary:\n{json.dumps(functions_dict, indent=2)}\n\n"
        f"Math blocks:\n{json.dumps(math_blocks, indent=2)}\n\n"
        "Please convert the above math blocks into a JSON list of wrapper nodes."
    )

    messages = [
        {"role": "system", "content": system_instructions},
        {"role": "user", "content": user_instructions}
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=messages,
            temperature=0
        )
        reply_content = response.choices[0].message["content"].strip()
        wrappers = json.loads(reply_content)
        return wrappers
    except Exception as e:
        print("Error during conversion:", e)
        return None

def main():
    math_blocks = extract_math_blocks(INPUT_FILE)
    if not math_blocks:
        print("No math blocks found in the input file.")
        return
    wrappers = convert_math_blocks_to_wrappers(math_blocks)
    if wrappers is None:
        print("Conversion failed.")
        return
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(wrappers, f, indent=2, ensure_ascii=False)
    print(f"Math wrappers have been saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
