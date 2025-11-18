import json
from datetime import datetime

def export_chat_json(chat_history, filename="chat_export.json"):
    """Export chat history as JSON with timestamps."""
    for msg in chat_history:
        if "timestamp" not in msg:
            msg["timestamp"] = datetime.now().isoformat()
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(chat_history, f, indent=2)
    return filename

def export_chat_markdown(chat_history, filename="chat_export.md"):
    """Export chat history as Markdown."""
    md_lines = []
    for msg in chat_history:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        timestamp = msg.get("timestamp", "")
        md_lines.append(f"**{role.title()}** ({timestamp}):\n{content}\n")
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
    return filename
