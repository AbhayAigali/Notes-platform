# generate_notes_json.py
import os
import json
from pathlib import Path

notes_dir = Path("notes")
out_file = Path("data/notes.json")

result = {}

# if notes/ has subfolders (subjects)
for subject_dir in sorted(notes_dir.iterdir()):
    if subject_dir.is_dir():
        subject = subject_dir.name
        result[subject] = []
        for f in sorted(subject_dir.iterdir()):
            if f.suffix.lower() == ".pdf":
                size = f.stat().st_size
                # human readable size
                for unit in ['B','KB','MB','GB']:
                    if size < 1024.0:
                        readable = f"{size:.2f} {unit}"
                        break
                    size /= 1024.0
                result[subject].append({
                    "name": f.name,
                    "file": str(f.as_posix()),
                    "size": readable
                })
# if notes/ contains PDFs directly (no subjects) put them under "General"
if not any(p.is_dir() for p in notes_dir.iterdir()):
    result["General"] = []
    for f in sorted(notes_dir.iterdir()):
        if f.suffix.lower() == ".pdf":
            size = f.stat().st_size
            s = size
            for unit in ['B','KB','MB','GB']:
                if s < 1024.0:
                    readable = f"{s:.2f} {unit}"
                    break
                s /= 1024.0
            result["General"].append({
                "name": f.name,
                "file": str(f.as_posix()),
                "size": readable
            })

out_file.parent.mkdir(parents=True, exist_ok=True)
out_file.write_text(json.dumps(result, indent=2))
print("Wrote", out_file)
