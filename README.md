# Pint Challenge Leaderboard

This repository powers a simple leaderboard site for the "Pint Challenge" community and includes a helper script to process WhatsApp chat exports into a CSV file the site can read.

## Project contents
- `index.html` – Static page that fetches `data.csv` to display the latest pint number, last contributor, and a leaderboard.
- `code.py` – Parses `chat.txt` exports from WhatsApp and writes a normalized `data.csv` with timestamps, sender names, pint numbers, and optional photo filenames.
- `media/` – Folder where photo attachments referenced in the chat export can be placed.
- `data.csv` and `chat.txt` – Example data inputs/outputs used by the parser and site.

## Running the parser
1. Place your WhatsApp-exported chat text file at `chat.txt` and any referenced images in the `media/` folder.
2. Run the parser with Python 3:
   ```bash
   python code.py
   ```
3. The script will produce or overwrite `data.csv` with normalized rows and print how many entries were parsed.

## Viewing the leaderboard locally
Open `index.html` in a browser after generating `data.csv`. The page fetches `data.csv` from `https://pint.hsho.me/data.csv` by default; adjust `csvUrl` in the script if you want to load a local file.

## Notes
- The parser searches up to five lines above each pint entry for a matching photo line (e.g., `<attached: filename.jpg>`) and records the filename if the image exists in `media/`.
- The leaderboard aggregates pint counts per sender and shows the top 15 contributors.
