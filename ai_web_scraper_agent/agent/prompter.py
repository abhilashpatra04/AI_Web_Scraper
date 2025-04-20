import re

def parse_prompt(prompt):
    prompt = prompt.lower()

    if "hacker news" in prompt:
        return {"type": "hacker_news"}

    if "train" in prompt or "schedule" in prompt or "timing" in prompt or "fare" in prompt:
        match = re.search(r"from\s+(\w+)\s+to\s+(\w+)", prompt)
        if match:
            source = match.group(1)
            destination = match.group(2)
            return {"type": "train_schedule", "source": source, "destination": destination}
        else:
            return {"type": "train_schedule", "source": None, "destination": None}

    return {"type": "unknown"}
