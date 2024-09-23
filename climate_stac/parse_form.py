import re

def parse_md_to_dict(md_content):
    data = {}
    current_key = None

    for line in md_content.split('\n'):

        # skip '_No response_', 'None' or empty lines
        if line.strip() in ['_No response_', 'None', '']:
            continue

        header_match = re.match(r'### (.+)', line)
        
        if header_match:
            current_key = header_match.group(1).strip()
            data[current_key] = None
        elif current_key:
            if data[current_key] is None:
                data[current_key] = ""

            data[current_key] += line.strip()

    return data


if __name__ == '__main__':
    with open('csv/test_form.md', 'r') as f:
        md_content = f.read()

    print(parse_md_to_dict(md_content))