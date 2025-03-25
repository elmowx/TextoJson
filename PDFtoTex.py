import os
import json
import time
import zipfile
import requests
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def convert_pdf_to_latex(pdf_filepath):
    try:
        load_dotenv()
        
        app_id = os.getenv('MATHPIX_APP_ID')
        app_key = os.getenv('MATHPIX_APP_KEY')
                
        if not os.path.exists(pdf_filepath):
            return f"Error: File {pdf_filepath} does not exist"
        
        if not pdf_filepath.lower().endswith('.pdf'):
            return "Error: Please provide a PDF file"
        
        logger.info(f"Processing PDF file: {pdf_filepath}")
        
        headers = {
            "app_id": app_id,
            "app_key": app_key
        }
        
        options = {
            "conversion_formats": {
                "tex.zip": True
            },
            "math_inline_delimiters": ["$", "$"],
            "rm_spaces": True
        }
        
        with open(pdf_filepath, 'rb') as pdf_file:
            files = {
                'file': pdf_file,
                'options_json': (None, json.dumps(options))
            }
            
            logger.info("Uploading PDF to Mathpix API...")
            response = requests.post(
                "https://api.mathpix.com/v3/pdf",
                headers=headers,
                files=files
            )
        
        if response.status_code != 200:
            return f"PDF upload failed: {response.text}"
        
        pdf_id = response.json().get('pdf_id')
        if not pdf_id:
            return "No PDF ID received"
        
        logger.info(f"PDF uploaded successfully. PDF ID: {pdf_id}")
        
        logger.info("Waiting for PDF processing...")
        while True:
            status_response = requests.get(
                f"https://api.mathpix.com/v3/pdf/{pdf_id}",
                headers=headers
            )
            
            if status_response.status_code != 200:
                return f"Status check failed: {status_response.text}"
            
            status_data = status_response.json()
            
            if status_data.get('status') == 'completed':
                logger.info("PDF processing completed")
                break
                
            logger.info("PDF still processing, waiting...")
            time.sleep(2)
        
        logger.info("Waiting for PDF conversion...")
        while True:
            conv_response = requests.get(
                f"https://api.mathpix.com/v3/converter/{pdf_id}",
                headers=headers
            )
            
            if conv_response.status_code != 200:
                return f"Conversion check failed: {conv_response.text}"
            
            conv_data = conv_response.json()
            
            if conv_data.get('status') == 'completed':
                logger.info("PDF conversion completed")
                break
                
            logger.info("Conversion still in progress, waiting...")
            time.sleep(2)
        
        logger.info("Downloading LaTeX content...")
        tex_response = requests.get(
            f"https://api.mathpix.com/v3/pdf/{pdf_id}.tex",
            headers=headers
        )
        
        if tex_response.status_code != 200:
            return f"LaTeX download failed: {tex_response.text}"
        
        os.makedirs('output', exist_ok=True)
        
        zip_path = os.path.join('output', f'{pdf_id}.tex.zip')
        with open(zip_path, 'wb') as f:
            f.write(tex_response.content)
        
        logger.info(f"Downloaded LaTeX ZIP to {zip_path}")
        
        latex_content = ""
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            tex_files = [f for f in zip_ref.namelist() if f.endswith('.tex')]
            if tex_files:
                with zip_ref.open(tex_files[0]) as tex_file:
                    latex_content = tex_file.read().decode('utf-8')
        
        output_path = os.path.join('output', 'output.tex')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(latex_content)
        
        logger.info(f"LaTeX content saved to {output_path}")
        
        os.remove(zip_path)
        logger.info(f"Temporary ZIP file removed")
        
        return f"PDF converted to LaTeX successfully. Output saved to {output_path}"
        
    except Exception as e:
        logger.error(f"Error in convert_pdf_to_latex: {str(e)}")
        return f"Error: {str(e)}"

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_file = os.path.join(script_dir, "example.pdf")
    
    result = convert_pdf_to_latex(pdf_file)
    print(result)