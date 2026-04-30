import json
import re

def split_into_chunks(text, chunk_size=150):
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        words = sentence.split()
        if current_length + len(words) > chunk_size:
            if current_chunk:
                chunks.append(" ".join(current_chunk))
            current_chunk = words
            current_length = len(words)
        else:
            current_chunk.extend(words)
            current_length += len(words)

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

def determine_retained(chunk):
    keywords = [
        "memory", "retain", "forget", "recall", "expression",
        "reasoning", "trace", "interpret", "black box", "cognition",
        "working memory", "long-term", "selective", "attention", "decay"
    ]
    found = [kw for kw in keywords if kw.lower() in chunk.lower()]
    if found:
        return f"Core concepts retained: {', '.join(found[:3])}. " + chunk[:200]
    return chunk[:200]

def determine_forgotten(chunk):
    noise_phrases = [
        "et al", "arxiv", "doi", "preprint", "https", "figure",
        "table", "appendix", "citation", "footnote", "copyright"
    ]
    found = [p for p in noise_phrases if p.lower() in chunk.lower()]
    if found:
        return f"Filtered out: references, citations, technical metadata"
    return "No significant noise detected in this chunk"

def generate_reasoning_trace(chunk, title, topic):
    return (
        f"Reading this section from '{title}' under topic '{topic}'. "
        f"I identify the core argument being made. "
        f"I ask: what is essential here versus what is supporting detail? "
        f"The main claim is: {chunk[:150]}... "
        f"I hold this in working memory while checking if it connects to what I already know about {topic}."
    )

def generate_expression(chunk, topic):
    return (
        f"So basically what this is saying about {topic} is — "
        f"{chunk[:120]}... "
        f"which makes sense when you think about how humans naturally handle this kind of information."
    )

def generate_why(chunk, topic):
    keywords = ["memory", "forget", "retain", "reason", "express", "interpret", "trace"]
    matched = [k for k in keywords if k in chunk.lower()]
    if matched:
        return (
            f"This chunk was retained because it directly addresses "
            f"{', '.join(matched[:2])} — core pillars of the Expression Architecture. "
            f"It contributes to understanding how AI can express and manage information like humans."
        )
    return (
        f"This chunk provides supporting context for {topic}. "
        f"Retained for its relevance to the Expression Architecture framework."
    )

def format_dataset(papers):
    formatted = []

    for paper in papers:
        title = paper["title"]
        arxiv_id = paper["arxiv_id"]
        topic = paper["topic"]
        summary = paper["summary"]

        chunks = split_into_chunks(summary, chunk_size=100)

        for i, chunk in enumerate(chunks):
            if len(chunk.strip()) < 30:
                continue

            entry = {
                "source_paper": title,
                "arxiv_id": arxiv_id,
                "topic": topic,
                "chunk_id": f"{arxiv_id}_chunk_{i}",
                "input": chunk,
                "reasoning_trace": generate_reasoning_trace(chunk, title, topic),
                "expression": generate_expression(chunk, topic),
                "retained": determine_retained(chunk),
                "forgotten": determine_forgotten(chunk),
                "why": generate_why(chunk, topic)
            }

            formatted.append(entry)

    print(f"Total dataset entries generated: {len(formatted)}")
    return formatted

def save_to_jsonl(data, filepath="dataset.jsonl"):
    with open(filepath, "w", encoding="utf-8") as f:
        for entry in data:
            f.write(json.dumps(entry) + "\n")
    print(f"Dataset saved to {filepath}")