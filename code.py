from pathlib import Path
import re
import csv
from datetime import datetime

# Configurable paths
CHAT_FILE = Path("chat.txt")
MEDIA_DIR = Path("media")
OUTPUT_CSV = Path("data.csv")

# Regex pattern for parsing pint messages
PINT_LINE_RE = re.compile(r"\[(.*?)\] ~\s*(.*?): (\d{4,6})")
PHOTO_LINE_RE = re.compile(r"<attached: (.*?)>")

def parse_chat(chat_path: Path, media_dir: Path, output_csv: Path):
    if not chat_path.exists():
        print(f"Chat file not found: {chat_path}")
        return

    with open(chat_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    rows = []

    for i, line in enumerate(lines):
        match = PINT_LINE_RE.match(line)
        if match:
            timestamp_str, sender, number = match.groups()
            try:
                ts = datetime.strptime(timestamp_str, "%d/%m/%Y, %H:%M:%S")
            except ValueError:
                ts = datetime.now()

            photo_filename = ""
            # Look backward for a photo line within the last 5 lines
            for j in range(i - 1, max(i - 5, 0), -1):
                photo_match = PHOTO_LINE_RE.search(lines[j])
                if photo_match:
                    potential_photo = photo_match.group(1)
                    if (media_dir / potential_photo).exists():
                        photo_filename = potential_photo
                        break

            rows.append({
                "timestamp": ts.strftime("%Y-%m-%d %H:%M:%S"),
                "sender": sender,
                "number": int(number),
                "photo": photo_filename
            })

    # Write to CSV
    with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["timestamp", "sender", "number", "photo"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"✅ Parsed {len(rows)} entries into {output_csv}")

# Run the script
parse_chat(CHAT_FILE, MEDIA_DIR, OUTPUT_CSV)
