#!/usr/bin/python3
"""A script converting Markdown markup language files into HTML files"""

import hashlib
import os
import re
import sys


def replace_bold(match):
    """Returns a formatted bold string in HTML"""
    return f'<b>{match.group(1)}</b>'


def replace_em(match):
    """Returns a formatted emphasized string in HTML"""
    return f'<em>{match.group(1)}</em>'


def encode_md5(match):
    """Returns an MD5 hash of the matched string"""
    return hashlib.md5(match.group(1).encode()).hexdigest()


def remove_c(match):
    """Returns the string with all 'c' and 'C' characters removed"""
    return match.group(1).replace('c', '').replace('C', '')


def main():
    """Main function handling the conversion of Markdown to HTML"""

    if len(sys.argv) != 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    md_file = sys.argv[1]
    html_file = sys.argv[2]

    if not os.path.isfile(md_file):
        print(f"Missing {md_file}", file=sys.stderr)
        sys.exit(1)

    # Regular expression patterns
    pattern_bold = re.compile(r'\*\*(.*?)\*\*')
    pattern_em = re.compile(r'__(.*?)__')
    pattern_md5 = re.compile(r'\[\[(.*?)\]\]')
    pattern_c = re.compile(r'\(\((.*?)\)\)')

    with open(md_file, 'r', encoding='utf-8') as markdown, \
         open(html_file, 'w', encoding='utf-8') as html:

        ul_open = False
        ol_open = False
        p_open = False

        for line in markdown:
            line = line.rstrip('\n')

            # Close open blocks if necessary
            if ul_open and not line.startswith("-"):
                html.write("</ul>\n")
                ul_open = False
            if ol_open and not line.startswith("* "):
                html.write("</ol>\n")
                ol_open = False
            if p_open and (line.startswith("-") or
                           line.startswith("* ") or
                           line.startswith("#") or
                           line.strip() == ""):
                html.write("\n</p>\n")
                p_open = False

            # Reached end or empty line
            if not line.strip():
                continue

            # Apply inline transformations
            line = re.sub(pattern_bold, replace_bold, line)
            line = re.sub(pattern_em, replace_em, line)
            line = re.sub(pattern_md5, encode_md5, line)
            line = re.sub(pattern_c, remove_c, line)

            # Headings
            if line.startswith("#"):
                count = len(line) - len(line.lstrip("#"))
                text = line.lstrip("#").strip()
                html.write(f"<h{count}>{text}</h{count}>\n")

            # Unordered list
            elif line.startswith("-"):
                if not ul_open:
                    html.write("<ul>\n")
                    ul_open = True
                text = line.lstrip("-").strip()
                html.write(f"<li>{text}</li>\n")

            # Ordered list
            elif line.startswith("* "):
                if not ol_open:
                    html.write("<ol>\n")
                    ol_open = True
                text = line.lstrip("* ").strip()
                html.write(f"<li>{text}</li>\n")

            # Paragraphs
            else:
                if not p_open:
                    html.write("<p>\n")
                    p_open = True
                else:
                    html.write("\n<br/>\n")
                html.write(line.strip())

        # Final cleanup for any unclosed tags
        if p_open:
            html.write("\n</p>\n")
        if ul_open:
            html.write("</ul>\n")
        if ol_open:
            html.write("</ol>\n")

    sys.exit(0)


if __name__ == "__main__":
    main()
