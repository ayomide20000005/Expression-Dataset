import requests
import xml.etree.ElementTree as ET
import json
import os

ARXIV_IDS = [
    # Topic 1 — Human Memory & AI Memory
    ("2504.15965", "Human Memory & AI Memory"),
    ("2603.15994", "Human Memory & AI Memory"),
    ("2512.06616", "Human Memory & AI Memory"),
    ("2310.03052", "Human Memory & AI Memory"),
    ("2411.00489", "Human Memory & AI Memory"),
    ("2601.18642", "Human Memory & AI Memory"),
    ("2508.13171", "Human Memory & AI Memory"),
    ("2404.13501", "Human Memory & AI Memory"),
    ("2502.12110", "Human Memory & AI Memory"),
    ("2603.07670", "Human Memory & AI Memory"),
    ("2312.17259", "Human Memory & AI Memory"),
    ("2408.09559", "Human Memory & AI Memory"),
    ("2409.12524", "Human Memory & AI Memory"),
    ("2410.15665", "Human Memory & AI Memory"),
    ("2512.20651", "Human Memory & AI Memory"),

    # Topic 2 — Reasoning Traces
    ("2503.08679", "Reasoning Traces"),
    ("2602.14903", "Reasoning Traces"),
    ("2511.22176", "Reasoning Traces"),
    ("2603.12397", "Reasoning Traces"),
    ("2508.14828", "Reasoning Traces"),
    ("2510.09312", "Reasoning Traces"),
    ("2309.15402", "Reasoning Traces"),
    ("2505.16067", "Reasoning Traces"),
    ("2412.15266", "Reasoning Traces"),
    ("2501.09959", "Reasoning Traces"),
    ("2306.07174", "Reasoning Traces"),
    ("2408.09176", "Reasoning Traces"),
    ("2505.05410", "Reasoning Traces"),
    ("2411.15114", "Reasoning Traces"),
    ("2602.14903", "Reasoning Traces"),

    # Topic 3 — Expression, Black Box & Interpretability
    ("2511.19265", "Expression & Interpretability"),
    ("2503.21356", "Expression & Interpretability"),
    ("2603.23251", "Expression & Interpretability"),
    ("2411.08010", "Expression & Interpretability"),
    ("2407.03646", "Expression & Interpretability"),
    ("2501.05032", "Expression & Interpretability"),
    ("2504.14706", "Expression & Interpretability"),
    ("2403.05175", "Expression & Interpretability"),
    ("2507.10485", "Expression & Interpretability"),
    ("2410.21815", "Expression & Interpretability"),
    ("2009.13996", "Expression & Interpretability"),
    ("2102.11343", "Expression & Interpretability"),
    ("2205.09029", "Expression & Interpretability"),
    ("2001.01578", "Expression & Interpretability"),
    ("2310.11511", "Expression & Interpretability"),
    ("2404.16130", "Expression & Interpretability"),
    ("2305.14322", "Expression & Interpretability"),
    ("2406.18312", "Expression & Interpretability"),
    ("2405.14831", "Expression & Interpretability"),
    ("2502.14437", "Expression & Interpretability"),
]

def fetch_papers():
    papers = []
    base_url = "https://export.arxiv.org/api/query?id_list="

    print("Fetching papers from Arxiv...")

    for arxiv_id, topic in ARXIV_IDS:
        try:
            url = base_url + arxiv_id
            response = requests.get(url)
            root = ET.fromstring(response.content)

            namespace = {"atom": "http://www.w3.org/2005/Atom"}
            entry = root.find("atom:entry", namespace)

            if entry is not None:
                title = entry.find("atom:title", namespace).text.strip()
                summary = entry.find("atom:summary", namespace).text.strip()

                paper = {
                    "arxiv_id": arxiv_id,
                    "title": title,
                    "summary": summary,
                    "topic": topic
                }

                # Save raw paper
                raw_path = os.path.join("raw", f"{arxiv_id}.json")
                with open(raw_path, "w") as f:
                    json.dump(paper, f)

                papers.append(paper)
                print(f"✓ [{topic}] {title[:60]}...")

        except Exception as e:
            print(f"✗ Failed to fetch {arxiv_id}: {e}")

    print(f"\nTotal papers fetched: {len(papers)}")
    return papers