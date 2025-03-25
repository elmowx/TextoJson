import json
import re

input_file = r"C:\Users\kecko\Documents\corc\output\output3.tex"
output_file = r"C:\Users\kecko\Documents\corc\output\output4.json"

def parse_blocks(file_path):
    blocks = []
    current_block = None
    block_type = None

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            text_match = re.match(r'^text block\s*\d+:', line, re.IGNORECASE)
            math_match = re.match(r'^math block\s*\d+:', line, re.IGNORECASE)
            if text_match:
                if current_block is not None:
                    blocks.append({"type": block_type, "content": current_block.strip()})
                block_type = "text"
                current_block = ""
            elif math_match:
                if current_block is not None:
                    blocks.append({"type": block_type, "content": current_block.strip()})
                block_type = "math"
                current_block = ""
            else:
                if current_block is not None:
                    current_block += line + " "
        if current_block is not None:
            blocks.append({"type": block_type, "content": current_block.strip()})
    return blocks

def create_wrapper(wrapper_id):
    return {
        "id": wrapper_id,
        "type": "wrapper",
        "props": {},
        "children": [
            {
                "type": "inline",
                "props": {},
                "children": []
            }
        ]
    }

def create_paragraph(text="", math_wrapper_id=""):
    children = []
    if text:
        children.append({
            "type": "text",
            "text": text
        })
    if math_wrapper_id:
        children.append({
            "type": "inlineExpression",
            "attributes": {
                "nodeId": math_wrapper_id,
                "isInline": True
            },
            "children": []
        })
    return {
        "type": "paragraph",
        "attributes": {},
        "children": children
    }

def process_blocks(blocks):
    math_wrappers = []
    text_nodes = []
    math_counter = 1
    i = 0
    while i < len(blocks):
        block = blocks[i]
        if block["type"] == "text":
            if i + 1 < len(blocks) and blocks[i+1]["type"] == "math":
                wrapper_id = f"wrapperId{math_counter}"
                math_counter += 1
                wrapper = create_wrapper(wrapper_id)
                math_wrappers.append(wrapper)
                paragraph_node = create_paragraph(text=block["content"], math_wrapper_id=wrapper_id)
                text_nodes.append(paragraph_node)
                i += 2
            else:
                paragraph_node = create_paragraph(text=block["content"])
                text_nodes.append(paragraph_node)
                i += 1
        elif block["type"] == "math":
            wrapper_id = f"wrapperId{math_counter}"
            math_counter += 1
            wrapper = create_wrapper(wrapper_id)
            math_wrappers.append(wrapper)
            paragraph_node = create_paragraph(math_wrapper_id=wrapper_id)
            text_nodes.append(paragraph_node)
            i += 1
    return math_wrappers, text_nodes

def main():
    blocks = parse_blocks(input_file)
    math_wrappers, text_nodes = process_blocks(blocks)
    output_json = {
        "nodes": [
            {
                "id": "textNode",
                "type": "text",
                "props": {},
                "children": math_wrappers
            }
        ],
        "textNode": text_nodes
    }
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_json, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()
