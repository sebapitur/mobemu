import re

def convert_fig_line(input_line):
    # Regular expression to parse the \fig line
    pattern = r"""\\fig\[
                    (.*?)     # options inside []
                   \]
                   \{
                    (.*?)     # image path
                   \}
                   \{
                    (.*?)     # label
                   \}
                   \{
                    (.*?)     # caption
                   \}"""

    # Use re.VERBOSE to allow multi-line regex
    match = re.match(pattern, input_line.strip(), re.VERBOSE)

    if match:
        options = match.group(1)
        image_path = match.group(2)
        label = match.group(3).strip()
        caption = match.group(4)


        if "{" in caption:
            caption += '}'

        # Create new figure block
        new_block = f"""\\begin{{figure}}[h!]
  \\centering
  \\includegraphics[{options}]{{{image_path}}}
  \\caption{{{caption}}}
  \\label{{{label}}}
\\end{{figure}}"""

        return new_block
    else:
        return "No match found. Check the input format."

def main():
    print("Paste your LaTeX \\fig lines one by one (Ctrl+C to exit):\n")
    while True:
        try:
            input_line = input()
            result = convert_fig_line(input_line)
            print("\nConverted LaTeX figure block:\n")
            print(result)
            print("\n" + "-"*60 + "\n")
        except KeyboardInterrupt:
            print("\nExiting.")
            break

if __name__ == "__main__":
    main()
