import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
from dotenv import load_dotenv

load_dotenv()


def preprocess_latex(latex_code: str):
    prompt = (
        "I will provide you with LaTeX code. Your task is to preprocess it by following these steps and reply just with updated version of the file as a plain text without anything else:\n\n"
        "1. Remove unnecessary elements\n"
        "   - Strip all \\usepackage{...} commands.\n"
        "   - Remove \\documentclass{...}, \\begin{document}, \\end{document}, \\title{...}, \\author{...}, and similar document setup commands.\n\n"
        "2. Flatten nested environments\n"
        "   - Remove any \\begin{...} and \\end{...} blocks, keeping only the raw content inside.\n"
        "   - This includes \\begin{align}, \\begin{equation}, \\begin{itemize}, etc.\n\n"
        "3. Reformat equations\n"
        "   - Convert all inline equations (\\( ... \\)) and display equations (\\[ ... \\]) into dollar signs ($ ... $).\n"
        "   - Ensure that all equations are correctly formatted without losing mathematical content and remwove all \\ from the end of the lines.\n\n"
        "4. Keep only text and equations\n"
        "   - Preserve only the main body content and equations.\n"
        "   - Discard tables, figures, references, and any other LaTeX-specific structures.\n\n"
        f"Here is the LaTeX code:\n```latex\n{latex_code}\n```")
    try:
        response = client.chat.completions.create(model="o3-mini",
        messages=[{
            "role": "system",
            "content": "You are an expert LaTeX processor."
        }, {
            "role": "user",
            "content": prompt
        }])
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error: {e}")
        return None


input_path = "output/output.tex"
output_path = "output/output2.tex"

try:
    with open(input_path, "r", encoding="utf-8") as file:
        latex_code = file.read()

    output = preprocess_latex(latex_code)

    if output:
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(output)
        print(f"Processed LaTeX saved to: {output_path}")
    else:
        print("Failed to process LaTeX.")
except Exception as e:
    print(f"Error reading/writing files: {e}")
