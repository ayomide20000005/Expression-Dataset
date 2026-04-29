import requests
import xml.etree.ElementTree as ET

ARXIV_IDS = [
    "2504.15965",  # From Human Memory to AI Memory
    "2603.15994",  # Selective Memory: Write-Time Gating
    "2512.06616",  # Memory Power Asymmetry in Human-AI
    "2503.08679",  # Chain-of-Thought Reasoning in the Wild
    "2602.14903",  # Reasoning Trace Dynamics
    "2511.22176",  # Focused Chain-of-Thought
    "2603.12397",  # Reasoning Traces Causally Shape Generalization
    "2508.14828",  # Long Chain-of-Thought Reasoning
    "2511.19265",  # Unboxing the Black Box
    "2503.21356",  # Interpretability vs Explainability
]

def fetch_papers():
    papers = []
    base_url = "https://export.arxiv.org/api/query?id_list="
    
    print("Fetching papers from Arxiv...")
    
    for arxiv_id in ARXIV_IDS:
        try:
            url = base_url + arxiv_id
            response = requests.get(url)
            root = ET.fromstring(response.content)
            
            namespace = {"atom": "http://www.w3.org/2005/Atom"}
            entry = root.find("atom:entry", namespace)
            
            if entry is not None:
                title = entry.find("atom:title", namespace).text.strip()
                summary = entry.find("atom:summary", namespace).text.strip()
                
                papers.append({
                    "arxiv_id": arxiv_id,
                    "title": title,
                    "summary": summary
                })
                print(f"✓ Fetched: {title[:60]}...")
            
        except Exception as e:
            print(f"✗ Failed to fetch {arxiv_id}: {e}")
    
    print(f"\nTotal papers fetched: {len(papers)}")
    return papers