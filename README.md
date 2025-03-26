# TextoJson


1. PDFtoTex.py
mathpix pdf to tex
input: PDF
output: tex
2. TexGPT.py
preprocess tex with chatgpt api
input: tex
output: tex
3. TexSplitter.py
split preprocessed tex for text and math blocks and replying with a sequence of separate blocks
input: tex
output: tex
4. JsonMath.py
fill json with text and create empty wrapper for math
input: tex
output: json
5. JsonMath.py
take math blocks from TexSplitter and send them to gpt to reply with separate wrappers for each of them
input: tex
output: json
6. JsonMerge.py
merge JsonMath and JsonMath, not finished
