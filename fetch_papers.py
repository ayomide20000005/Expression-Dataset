import json
import re

def split_into_chunks(text, chunk_size=200):
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

def determine_retained(chunk, title, topic):
    keywords = [
        "memory", "retain", "forget", "recall", "expression",
        "reasoning", "trace", "interpret", "black box", "cognition",
        "working memory", "long-term", "selective", "attention", "decay",
        "encoding", "retrieval", "storage", "salience", "compression"
    ]
    found = [kw for kw in keywords if kw.lower() in chunk.lower()]

    if found:
        return (
            f"From the paper '{title}', the following core concepts are retained as high-priority information: "
            f"{', '.join(found[:5])}. "
            f"These concepts are central to the Expression Architecture because they directly address how intelligent systems "
            f"manage, prioritize, and surface information the way humans naturally do. "
            f"Specifically, this chunk contributes to understanding {topic} by highlighting: {chunk[:300]}. "
            f"This information is flagged for long-term retention because it forms a foundational building block "
            f"for training models that express and reason like humans."
        )
    return (
        f"From '{title}', this chunk is retained as supporting context for {topic}. "
        f"While it does not directly reference the core memory or expression keywords, it provides "
        f"important background that helps ground the Expression Architecture in real research. "
        f"Content retained: {chunk[:300]}. "
        f"This is stored as secondary memory — available for retrieval when deeper context is needed."
    )

def determine_forgotten(chunk, topic):
    noise_phrases = [
        "et al", "arxiv", "doi", "preprint", "https", "figure",
        "table", "appendix", "citation", "footnote", "copyright",
        "submitted", "proceedings", "conference", "workshop"
    ]
    found = [p for p in noise_phrases if p.lower() in chunk.lower()]

    if found:
        return (
            f"The following elements have been filtered out as low-priority noise for the {topic} domain: "
            f"bibliographic references, citation markers, metadata tags, and publication details such as "
            f"{', '.join(found[:4])}. "
            f"These elements do not contribute to the reasoning or expressive quality of the dataset "
            f"and would introduce noise into model training. "
            f"In the same way a human reader skips footnotes and reference lists when trying to understand "
            f"the main argument, the Expression Architecture deliberately discards this peripheral information."
        )
    return (
        f"No significant noise was detected in this chunk from the {topic} domain. "
        f"Minor discarded elements include overly technical notation, redundant transitional phrases, "
        f"and filler language that does not contribute to the core argument. "
        f"The Expression Architecture treats these as low-salience signals — "
        f"they fade naturally from working memory without needing explicit removal."
    )

def generate_reasoning_trace(chunk, title, topic):
    return (
        f"I am processing a section from the paper '{title}', which falls under the topic of {topic}. "
        f"My first step is to identify what this section is actually claiming. "
        f"Reading carefully, the central argument appears to be: {chunk[:200]}. "
        f"I now ask myself — does this connect to what I already know about {topic}? "
        f"Yes, this builds on existing understanding by adding nuance around how information is processed, prioritized, and expressed. "
        f"I then consider what questions this raises: How does this mechanism compare to human cognition? "
        f"What would happen if this principle were applied to an AI system trying to express itself naturally? "
        f"I hold the key insight in working memory while I check for contradictions or supporting evidence. "
        f"The conclusion I reach is that this chunk is highly relevant to the Expression Architecture "
        f"because it directly informs how models should handle {topic} in a human-like way. "
        f"I flag this for retention and move forward with a clearer understanding of the concept."
    )

def generate_expression(chunk, topic):
    return (
        f"Okay so let me break this down in plain terms — this section is essentially saying that when it comes to {topic}, "
        f"there's something really important happening that most people overlook. "
        f"What the researchers found is: {chunk[:250]}. "
        f"Now if you think about how a human would naturally process this — "
        f"we don't store everything we read. We grab the parts that feel important, "
        f"connect them to things we already know, and let the rest fade. "
        f"That's exactly what the Expression Architecture is trying to replicate. "
        f"Instead of treating all information equally the way most AI systems do, "
        f"we want models that can say — this matters, this doesn't, here's why I think so — "
        f"and express that reasoning naturally, the way a thoughtful human would. "
        f"So this chunk is a good example of the kind of insight that should shape how we build that."
    )

def generate_why(chunk, topic):
    keywords = ["memory", "forget", "retain", "reason", "express", "interpret", "trace", "cognition", "selective", "decay"]
    matched = [k for k in keywords if k in chunk.lower()]

    if matched:
        return (
            f"This chunk was selected for retention because it directly addresses the following core pillars "
            f"of the Expression Architecture: {', '.join(matched[:4])}. "
            f"The Expression Architecture is built on three foundations — expression, reasoning traces, and memory behavior. "
            f"This chunk contributes to all three by demonstrating how {topic} research has approached "
            f"the problem of making intelligent systems more transparent and human-like. "
            f"Including this in the training dataset will help models learn to articulate their reasoning process, "
            f"decide what information deserves to be remembered versus discarded, "
            f"and express those decisions in a natural, human-like way. "
            f"This is exactly the kind of signal the Expression Architecture needs to function effectively."
        )
    return (
        f"This chunk was retained as supporting context for the {topic} domain within the Expression Architecture dataset. "
        f"Even though it does not directly reference the primary keywords, it provides important background "
        f"that helps situate the core concepts in a broader research landscape. "
        f"Training on diverse but relevant supporting content helps models develop a richer, "
        f"more nuanced understanding of how human-like expression and memory behavior manifest across different contexts. "
        f"This chunk strengthens the dataset's depth and helps prevent overfitting to only the most obvious signals."
    )

def format_dataset(papers):
    formatted = []

    for paper in papers:
        title = paper["title"]
        arxiv_id = paper["arxiv_id"]
        topic = paper["topic"]
        summary = paper["summary"]

        chunks = split_into_chunks(summary, chunk_size=200)

        for i, chunk in enumerate(chunks):
            if len(chunk.strip()) < 50:
                continue

            entry = {
                "source_paper": title,
                "arxiv_id": arxiv_id,
                "topic": topic,
                "chunk_id": f"{arxiv_id}_chunk_{i}",
                "input": (
                    f"From the research paper '{title}' on the topic of {topic}: {chunk}"
                ),
                "reasoning_trace": generate_reasoning_trace(chunk, title, topic),
                "expression": generate_expression(chunk, topic),
                "retained": determine_retained(chunk, title, topic),
                "forgotten": determine_forgotten(chunk, topic),
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