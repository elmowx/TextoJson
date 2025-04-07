import subprocess
import sys
import time
from pathlib import Path

def run_conversion_pipeline(pdf_path: str):
    scripts = [
        ("PDFtoTex.py", ["python", "PDFtoTex.py"], "output/output.tex"),
        ("TexGPT.py", ["python", "TexGPT.py"], "output/output2.tex"),
        ("TexSplitter.py", ["python", "TexSplitter.py"], "output/output3.tex"),
        ("JsonText.py", ["python", "JsonText.py"], "output/output4.json"),
        ("JsonMath.py", ["python", "JsonMath.py"], "output/output5.txt"),
        ("JsonMerge.py", ["python", "JsonMerge.py"], "output/output6.json")
    ]

    target_pdf = Path("example.pdf")
    if not target_pdf.exists():
        import shutil
        shutil.copy(pdf_path, target_pdf)

    for script_name, command, output_file in scripts:
        print(f"🟢 Running {script_name}...")
        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"🔴 Error in {script_name}:")
            print(result.stderr)
            sys.exit(1)

        if not Path(output_file).exists():
            print(f"🔴 {script_name} failed to create {output_file}")
            sys.exit(1)

        print(f"✅ {script_name} completed successfully")
        time.sleep(10)

    print("\n🎉 Completed!")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python app.py <path_to_pdf>")
        sys.exit(1)

    run_conversion_pipeline(sys.argv[1])
