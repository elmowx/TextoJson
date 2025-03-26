# TextoJson


1. PDFtoTex.py \n
mathpix pdf to tex
input: PDF
output: tex
2. TexGPT
preprocess tex with chatgpt api
input: tex
output: tex
3.TexSplitter
split preprocessed tex for text and math blocks and replying with a sequence of separate blocks
input: tex
output: tex
4. JsonMath
fill json with text and create empty wrapper for math
input: tex
output: json
6. JsonMath
take math blocks from TexSplitter and send them to gpt to reply with separate wrappers for each of them
input: tex
output: json
7. JsonMerge
merge JsonMath and JsonMath, not finished
