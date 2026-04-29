import json

def format_entry(paper):
    return {
        "input": paper.get("title", "") + " " + paper.get("summary", ""),
        "reasoning_trace": paper.get("summary", ""),
        "expression": paper.get("title", ""),
        "retained": paper.get("summary", "")[:300],
        "forgotten": "",
        "why": "Key concepts retained based on relevance to expression architecture"
    }

def format_dataset(papers):
    formatted = []
    for paper in papers:
        entry = format_entry(paper)
        formatted.append(entry)
    return formatted

def save_to_jsonl(data, filepath="dataset.jsonl"):
    with open(filepath, "w") as f:
        for entry in data:
            f.write(json.dumps(entry) + "\n")
    print(f"Dataset saved to {filepath}")