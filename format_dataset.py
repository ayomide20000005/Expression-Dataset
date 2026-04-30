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


def entry_memory_behavior(chunk, title, topic, arxiv_id, chunk_id):
    return {
        "source_paper": title,
        "arxiv_id": arxiv_id,
        "topic": topic,
        "chunk_id": f"{chunk_id}_memory",
        "entry_type": "memory_behavior",
        "input": f"Based on the research in '{title}' about {topic}, analyze the memory behavior described in the following passage and explain what should be retained, what should be forgotten, and why: {chunk}",
        "reasoning_trace": (
            f"I am reading a passage from '{title}' under the topic of {topic}. "
            f"My goal here is to analyze memory behavior — what deserves to stay in long-term memory and what should fade. "
            f"First I read the passage carefully: {chunk[:200]}. "
            f"I now ask myself: what is the single most important idea here? "
            f"I identify it and mark it as high salience — worth retaining. "
            f"Then I scan for supporting details, background context, and references — these are low salience. "
            f"I apply the same filter a human brain would: emotional relevance, novelty, and utility. "
            f"What remains after filtering is the core memory worth preserving for future reasoning."
        ),
        "expression": (
            f"So when you look at this passage from {topic} research, the key thing to understand is — "
            f"not everything in here deserves the same attention. "
            f"The really important part is: {chunk[:180]}. "
            f"A human reading this would naturally latch onto that and let the rest fade into the background. "
            f"That's exactly the kind of selective memory behavior the Expression Architecture is trying to teach AI systems. "
            f"Instead of storing everything equally, we want models that can say — this matters more than that — and act accordingly."
        ),
        "retained": (
            f"Core insight retained from '{title}': {chunk[:250]}. "
            f"This is flagged as high-priority memory because it directly informs how the Expression Architecture "
            f"models selective retention in AI systems under the {topic} domain. "
            f"This insight will be surfaced during reasoning when similar concepts arise in future inputs."
        ),
        "forgotten": (
            f"Discarded from this passage: redundant transitional phrases, citation markers, bibliographic references, "
            f"and any content that restates already established facts without adding new insight. "
            f"These elements are treated as low-salience noise — the same way a human reader naturally skips "
            f"footnotes and repetitive background context when trying to grasp the main argument."
        ),
        "why": (
            f"This chunk was retained under the memory behavior lens because it demonstrates a clear pattern "
            f"of how information should be prioritized in the {topic} domain. "
            f"The Expression Architecture requires training data that explicitly models the retain/forget decision — "
            f"this entry directly teaches that behavior by showing what matters and what doesn't in a real research context."
        )
    }


def entry_reasoning_trace(chunk, title, topic, arxiv_id, chunk_id):
    return {
        "source_paper": title,
        "arxiv_id": arxiv_id,
        "topic": topic,
        "chunk_id": f"{chunk_id}_reasoning",
        "entry_type": "reasoning_trace",
        "input": f"Walk through your step-by-step reasoning about the following passage from '{title}' on {topic}: {chunk}",
        "reasoning_trace": (
            f"Step 1 — I read the passage from '{title}' carefully. The passage says: {chunk[:200]}. "
            f"Step 2 — I identify the main claim. What is this passage actually arguing? "
            f"It appears to be making the case that {chunk[:100]}. "
            f"Step 3 — I check this against what I already know about {topic}. Does it align? Does it contradict? "
            f"Step 4 — I consider the implications. If this claim is true, what does it mean for how AI systems should behave? "
            f"Step 5 — I form a conclusion: this passage contributes meaningfully to understanding {topic} "
            f"by providing evidence that can inform the Expression Architecture's approach to reasoning transparency. "
            f"Step 6 — I flag this reasoning trace for inclusion in training data because it demonstrates "
            f"the kind of explicit, human-like thinking we want AI models to replicate."
        ),
        "expression": (
            f"Let me think through this out loud — this passage from {topic} is making a point that's actually really interesting. "
            f"It's saying: {chunk[:180]}. "
            f"My first reaction is — okay, that makes sense, but let me push on it a bit. "
            f"Why does this matter? Because if this is true, then AI systems that don't account for this "
            f"are missing something fundamental about how reasoning actually works. "
            f"The Expression Architecture is trying to close that gap — by making reasoning visible, "
            f"step by step, the way a thoughtful human would naturally explain their thinking."
        ),
        "retained": (
            f"Reasoning steps retained from this passage in '{title}': the main claim, the supporting evidence, "
            f"and the implication for {topic} research. Specifically: {chunk[:200]}. "
            f"These reasoning steps are stored as a structured trace that can be replayed and referenced "
            f"when the model encounters similar problems in the future."
        ),
        "forgotten": (
            f"Dropped from this reasoning trace: repetitive restatements of the same point, "
            f"overly technical notation that doesn't add reasoning value, "
            f"and background context that was already established earlier in the paper. "
            f"These are treated as noise in the reasoning chain — they slow down thinking without adding clarity."
        ),
        "why": (
            f"This reasoning trace entry was created because the Expression Architecture needs training data "
            f"that explicitly shows step-by-step human-like thinking. "
            f"This passage from '{title}' provides a strong anchor for that — "
            f"it contains enough substance to support a full reasoning chain across the {topic} domain, "
            f"making it ideal for teaching models to reason transparently and expressively."
        )
    }


def entry_expression(chunk, title, topic, arxiv_id, chunk_id):
    return {
        "source_paper": title,
        "arxiv_id": arxiv_id,
        "topic": topic,
        "chunk_id": f"{chunk_id}_expression",
        "entry_type": "expression",
        "input": f"Express the core idea from this passage in '{title}' about {topic} the way a knowledgeable human would naturally explain it to someone: {chunk}",
        "reasoning_trace": (
            f"I need to take this research content from '{title}' and express it naturally — "
            f"the way a human expert would explain it in conversation, not in academic language. "
            f"The passage says: {chunk[:180]}. "
            f"I first identify the core idea. Then I think about how I would actually say this to someone. "
            f"I strip away the jargon, find an analogy if possible, and make it feel alive and relatable. "
            f"The goal is expression — not just accuracy, but communication that resonates."
        ),
        "expression": (
            f"Okay so here's the thing about {topic} that this research is really getting at — "
            f"{chunk[:200]}. "
            f"Think about it this way: when you're trying to remember something important, "
            f"your brain doesn't treat everything equally. Some things stick, some things don't. "
            f"That's not random — there's a logic to it. And that's exactly what this research is unpacking. "
            f"The Expression Architecture takes this insight seriously — if we want AI to communicate like humans, "
            f"it needs to think and remember like humans too. Not perfectly, but naturally."
        ),
        "retained": (
            f"The expressive core of this passage from '{title}' retained for training: {chunk[:220]}. "
            f"This is stored as a high-quality expression example — it demonstrates how complex {topic} "
            f"concepts can be communicated naturally and accessibly without losing accuracy."
        ),
        "forgotten": (
            f"Stripped away for this expression entry: academic hedging language, passive voice constructions, "
            f"excessive qualification, and citation-heavy sentence structures. "
            f"These elements make research writing accurate but unnatural — "
            f"the Expression Architecture specifically trains against this pattern, "
            f"favoring direct, human-like communication instead."
        ),
        "why": (
            f"Expression is one of the three core pillars of the Expression Architecture. "
            f"This entry was created to provide direct training signal for how AI models should communicate "
            f"complex {topic} concepts in a natural, human-like way. "
            f"The passage from '{title}' was selected because it contains enough conceptual depth "
            f"to support rich expressive output while remaining grounded in real research."
        )
    }


def entry_black_box(chunk, title, topic, arxiv_id, chunk_id):
    return {
        "source_paper": title,
        "arxiv_id": arxiv_id,
        "topic": topic,
        "chunk_id": f"{chunk_id}_blackbox",
        "entry_type": "black_box_interpretability",
        "input": f"How does the following passage from '{title}' on {topic} help us understand or solve the black box problem in AI systems: {chunk}",
        "reasoning_trace": (
            f"I am examining this passage from '{title}' through the lens of AI interpretability. "
            f"The black box problem is about the gap between what AI systems do and what humans can understand about why they do it. "
            f"The passage states: {chunk[:200]}. "
            f"I ask — does this passage give us any insight into how AI decision-making can be made more transparent? "
            f"Yes — it points toward mechanisms that, if implemented, would make the internal reasoning of AI systems "
            f"more visible and understandable to human observers. "
            f"This connects directly to the Expression Architecture's goal of solving the black box problem "
            f"through expressive, traceable reasoning."
        ),
        "expression": (
            f"The black box problem is basically this — AI systems make decisions but we have no idea why. "
            f"It's like asking someone for directions and they just hand you a map with no explanation. "
            f"This passage from {topic} research is interesting because it starts to crack that open: "
            f"{chunk[:200]}. "
            f"What it's suggesting is that if we design systems that externalize their reasoning — "
            f"show their work, so to speak — we get closer to AI that humans can actually trust and understand. "
            f"That's the whole point of the Expression Architecture."
        ),
        "retained": (
            f"Retained from '{title}' for interpretability training: {chunk[:220]}. "
            f"This is flagged as critical content for the black box dimension of the Expression Architecture — "
            f"it provides direct evidence for how transparency and interpretability can be achieved in AI systems."
        ),
        "forgotten": (
            f"Discarded: implementation-specific technical details that don't generalize, "
            f"dataset-specific benchmarks that are too narrow, and experimental setup descriptions "
            f"that don't contribute to the interpretability argument. "
            f"The Expression Architecture needs principles, not just experimental results."
        ),
        "why": (
            f"Solving the black box problem is a core motivation of the Expression Architecture. "
            f"This entry was created to ensure the training dataset contains explicit signal "
            f"connecting {topic} research to interpretability goals. "
            f"The passage from '{title}' was selected because it directly engages with the question "
            f"of how AI systems can become more transparent and understandable."
        )
    }


def entry_human_vs_ai(chunk, title, topic, arxiv_id, chunk_id):
    return {
        "source_paper": title,
        "arxiv_id": arxiv_id,
        "topic": topic,
        "chunk_id": f"{chunk_id}_humanvsai",
        "entry_type": "human_vs_ai_comparison",
        "input": f"Compare how a human and an AI system would each handle the concept described in this passage from '{title}' on {topic}: {chunk}",
        "reasoning_trace": (
            f"I am comparing human and AI approaches to the concept described in '{title}'. "
            f"The passage describes: {chunk[:180]}. "
            f"A human encountering this would naturally: prioritize based on personal relevance, "
            f"connect it to prior experience, express uncertainty where it exists, "
            f"and communicate it in a way shaped by emotion and context. "
            f"A current AI system would: treat all tokens with equal initial weight, "
            f"retrieve statistically likely continuations, and produce output without genuine prioritization. "
            f"The Expression Architecture aims to close this gap — "
            f"by training on data that explicitly models human-like prioritization, expression, and memory behavior."
        ),
        "expression": (
            f"Here's a really interesting contrast when it comes to {topic}. "
            f"A human reading this passage — {chunk[:150]} — would immediately connect it to things they already know, "
            f"flag the surprising parts, and naturally forget the boring bits. "
            f"An AI system right now? It just processes everything equally, no real sense of what matters more. "
            f"That's the gap the Expression Architecture is trying to close. "
            f"We want AI that reads like a person — curious, selective, expressive — not like a search engine."
        ),
        "retained": (
            f"Retained for human-AI comparison training from '{title}': {chunk[:200]}. "
            f"This contrast is stored as a key training signal showing the gap between human cognitive behavior "
            f"and current AI system behavior in the {topic} domain."
        ),
        "forgotten": (
            f"Dropped: superficial similarities between human and AI behavior that don't reveal meaningful differences, "
            f"and technical implementation details that distract from the conceptual comparison. "
            f"The focus must stay on the cognitive and expressive gap, not the engineering details."
        ),
        "why": (
            f"The human-AI comparison is central to the Expression Architecture's motivation. "
            f"This entry was created to give the model explicit training signal on where the gap lies "
            f"and why closing it matters. The passage from '{title}' provides a concrete {topic} example "
            f"that grounds this comparison in real research rather than abstract claims."
        )
    }


def entry_application(chunk, title, topic, arxiv_id, chunk_id):
    return {
        "source_paper": title,
        "arxiv_id": arxiv_id,
        "topic": topic,
        "chunk_id": f"{chunk_id}_application",
        "entry_type": "architecture_application",
        "input": f"How would the Expression Architecture apply the insight from this passage in '{title}' on {topic} to build better AI systems: {chunk}",
        "reasoning_trace": (
            f"I am reading '{title}' and asking — how does this apply to the Expression Architecture specifically? "
            f"The passage states: {chunk[:200]}. "
            f"I identify the core insight and then trace its implications for system design. "
            f"If the Expression Architecture were to incorporate this insight, it would need to: "
            f"first, encode this principle into its memory management layer; "
            f"second, reflect it in how the model generates reasoning traces; "
            f"third, express it naturally when communicating outputs to users. "
            f"This is how research insights from {topic} translate into architectural decisions."
        ),
        "expression": (
            f"So if we're building the Expression Architecture and we come across this insight from {topic} — "
            f"{chunk[:180]} — the question is, how do we actually use this? "
            f"The answer is: we bake it into how the model decides what to remember, "
            f"how it explains its thinking, and how it talks about what it knows and doesn't know. "
            f"Research like this isn't just theory — it's the blueprint for building AI that actually behaves like a thoughtful human being."
        ),
        "retained": (
            f"Architectural insight retained from '{title}': {chunk[:220]}. "
            f"This is stored as a design principle for the Expression Architecture — "
            f"it informs specific decisions about memory management, reasoning trace generation, "
            f"and expressive output in the {topic} domain."
        ),
        "forgotten": (
            f"Dropped: experimental results that are too dataset-specific to generalize, "
            f"implementation details tied to specific hardware or frameworks, "
            f"and theoretical proofs that don't translate into practical architectural decisions. "
            f"The Expression Architecture needs actionable principles, not just academic validation."
        ),
        "why": (
            f"The Expression Architecture is not just a theoretical framework — it needs to be built. "
            f"This entry was created to provide direct training signal connecting {topic} research insights "
            f"to concrete architectural decisions. "
            f"The passage from '{title}' was selected because it contains a clear, applicable insight "
            f"that can inform how the Expression Architecture is designed and implemented."
        )
    }


def format_dataset(papers):
    formatted = []

    for paper in papers:
        title = paper["title"]
        arxiv_id = paper["arxiv_id"]
        topic = paper["topic"]
        content = paper.get("full_text", paper.get("summary", ""))

        chunks = split_into_chunks(content, chunk_size=150)

        for i, chunk in enumerate(chunks):
            if len(chunk.strip()) < 50:
                continue

            chunk_id = f"{arxiv_id}_chunk_{i}"

            formatted.append(entry_memory_behavior(chunk, title, topic, arxiv_id, chunk_id))
            formatted.append(entry_reasoning_trace(chunk, title, topic, arxiv_id, chunk_id))
            formatted.append(entry_expression(chunk, title, topic, arxiv_id, chunk_id))
            formatted.append(entry_black_box(chunk, title, topic, arxiv_id, chunk_id))
            formatted.append(entry_human_vs_ai(chunk, title, topic, arxiv_id, chunk_id))
            formatted.append(entry_application(chunk, title, topic, arxiv_id, chunk_id))

    print(f"Total dataset entries generated: {len(formatted)}")
    return formatted


def save_to_jsonl(data, filepath="dataset.jsonl"):
    with open(filepath, "w", encoding="utf-8") as f:
        for entry in data:
            f.write(json.dumps(entry) + "\n")
    print(f"Dataset saved to {filepath}")