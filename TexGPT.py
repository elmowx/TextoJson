import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def preprocess_latex(latex_code: str):
    prompt = f"""
    I will provide you with LaTeX code. Your task is to preprocess it by following these steps:

    1. Remove unnecessary elements
       - Strip all \usepackage{{...}} commands.
       - Remove \documentclass{{...}}, \begin{{document}}, \end{{document}}, \title{{...}}, \author{{...}}, and similar document setup commands.

    2. Flatten nested environments
       - Remove any \begin{{...}} and \end{{...}} blocks, keeping only the raw content inside.
       - This includes \begin{{align}}, \begin{{equation}}, \begin{{itemize}}, etc.

    3. Reformat equations
       - Convert all inline equations (\( ... \)) and display equations (\[ ... \]) into dollar signs ($ ... $).
       - Ensure that all equations are correctly formatted without losing mathematical content.

    4. Keep only text and equations
       - Preserve only the main body content and equations.
       - Discard tables, figures, references, and any other LaTeX-specific structures.

    Here is the LaTeX code:
    ```latex
    {latex_code}
    ```
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert LaTeX processor."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=1000
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"Error: {e}")
        return None

input_path = "C:\\Users\\kecko\\Documents\\corc\\output\\output.tex"
output_path = "C:\\Users\\kecko\\Documents\\corc\\output\\output2.tex"

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