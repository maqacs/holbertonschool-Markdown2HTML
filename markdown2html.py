#!/usr/bin/python3
"""A script converting Markdown markup language files into HTML files"""

import hashlib
import os
import re
import sys


def replace_bold(match):
    """A function that returns a formatted bold string html"""
    bold_text = match.group(1)
    return f'<b>{bold_text}</b>'


def replace_em(match):
    """A function that returns a formatted em string html"""
    em_text = match.group(1)
    return f'<em>{em_text}</em>'


def encode_md5(match):
    """A function that returns a MD5 encoded string"""
    text_to_encode = match.group(1)
    return hashlib.md5(text_to_encode.encode()).hexdigest()


def remove_c(match):
    """A function that returns a string without "c" characters"""
    text_with_c = match.group(1)
    return text_with_c.replace('c', '').replace('C', '')


def main():
    """The main function running the script

    Raises:
            "Usage: ./markdown2html.py README.md README.html" to STDERR:
            If the number of arguments in the CLI is different of 2
            "Missing <filename>" to STDERR: If the Markdown file doesn’t exist
    """

    # Checking if number of CLI arguments is wright
    if len(sys.argv) != 3:
        print("Usage: ./markdown2html.py README.md README.html",
              file=sys.stderr)
        sys.exit(1)

    md_file = sys.argv[1]
    html_file = sys.argv[2]

    # Checking if markdown file exists
    if not os.path.isfile(md_file):
        print(f"Missing {md_file}", file=sys.stderr)
        sys.exit(1)

    # Parsing the markdown file and writing html to a new html file
    with open(md_file, "r", encoding='UTF-8') as markdown:
        with open(html_file, "w", encoding='UTF-8') as html:

            # HTML tags
            ol_open = False
            ul_open = False
            p_open = False

            # Special patterns
            pattern_bold = re.compile(r'\*\*(.*?)\*\*')
            pattern_em = re.compile(r'__(.*?)__')
            pattern_md5 = re.compile(r'\[\[(.*?)\]\]')
            pattern_c = re.compile(r'\(\((.*?)\)\)')

            # The loop to parse the file
            while True:
                line = markdown.readline()

                # Checks if we are in an ul
                if ul_open and not line.startswith("-"):
                    html.write("</ul>\n")
                    ul_open = False

                # Checks if we are in an ol
                if ol_open and not line.startswith("* "):
                    html.write("</ol>\n")
                    ol_open = False

                # Checks if we are in a paragraph
                if p_open and (line.startswith("-") or
                               line.startswith("* ,") or
                               line.startswith("#") or
                               line.startswith("\n")):
                    html.write("</p>\n")
                    p_open = False

                # Reaches the EOF
                if not line:
                    break

                # Evaluation em, bold, md5, strip "c"
                # chars contents in the line
                line = re.sub(pattern_bold, replace_bold, line)
                line = re.sub(pattern_em, replace_em, line)
                line = re.sub(pattern_md5, encode_md5, line)
                line = re.sub(pattern_c, remove_c, line)

                # Generates Headings
                if line.startswith("#"):
                    count = line.count("#")
                    text = line.rsplit('# ', 1)[1].strip()
                    html.write(f"<h{count}>{text}</h{count}>\n")

                # Generates unordered listing
                elif line.startswith("-"):
                    if not ul_open:
                        html.write("<ul>\n")
                        ul_open = True
                    text = line.rsplit('- ', 1)[1].strip()
                    html.write(f"<li>{text}</li>\n")

                # Generates ordered listing
                elif line.startswith('* '):
                    if not ol_open:
                        html.write("<ol>\n")
                        ol_open = True
                    text = line.rsplit('* ', 1)[1].strip()
                    html.write(f"<li>{text}</li>\n")

                # Generates paragraphs
                elif not line.startswith("\n"):
                    if not p_open:
                        html.write("<p>\n")
                        p_open = True
                    else:
                        html.write("<br/>\n")
                    text = line
                    html.write(text)

    # Exits after sucessful program execution
    sys.exit()


if __name__ == "__main__":
    main()