#!/usr/bin/python3
import os
import sys
import re

def convert_markdown_to_html(markdown_text):
    html_lines = []
    lines = markdown_text.splitlines()

    for line in lines:
        # Headers
        if line.startswith('#'):
            header_level = len(line) - len(line.lstrip('#'))
            header_text = line.lstrip('#').strip()
            html_lines.append(f"<h{header_level}>{header_text}</h{header_level}>")
        elif line.strip() == '':
            continue  # skip empty lines
        else:
            # Convert bold and italic
            line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
            line = re.sub(r'\*(.*?)\*', r'<em>\1</em>', line)
            html_lines.append(f"<p>{line}</p>")

    return '\n'.join(html_lines)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.isfile(input_file):
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(input_file, 'r') as f:
            markdown_content = f.read()

        html_content = convert_markdown_to_html(markdown_content)

        with open(output_file, 'w') as f:
            f.write(html_content)

        sys.exit(0)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)