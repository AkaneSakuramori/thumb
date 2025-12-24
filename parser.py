import re

def parse_info(text: str) -> dict:
    data = {}
    lines = text.strip().splitlines()

    title_line = lines[0]
    if "|" in title_line:
        data["title"], data["alt_title"] = map(str.strip, title_line.split("|"))
    else:
        data["title"] = title_line

    for line in lines:
        match = re.match(r"‣\s*(.+?)\s*:\s*(.+)", line)
        if match:
            key, value = match.groups()
            data[key.lower().replace(" ", "_")] = value.strip()

    return data
