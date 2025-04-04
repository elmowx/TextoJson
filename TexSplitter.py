import re


def separate_tex_blocks():
    input_path = "output/output2.tex"
    output_path = "output/output3.tex"

    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    segments = re.split(r'\$', content)

    output_lines = []
    text_block_count = 0
    math_block_count = 0

    for i, segment in enumerate(segments):
        segment = segment.strip()
        if not segment:
            continue

        if i % 2 == 0:
            text_block_count += 1
            output_lines.append(f"text block {text_block_count}:")
            output_lines.append(segment)
        else:
            math_block_count += 1
            output_lines.append(f"math block {math_block_count}:")
            output_lines.append(segment)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(output_lines))

    print(f"Blocks have been written to {output_path}")


if __name__ == "__main__":
    separate_tex_blocks()
