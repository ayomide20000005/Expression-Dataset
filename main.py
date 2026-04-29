from fetch_papers import fetch_papers
from format_dataset import format_dataset, save_to_jsonl
from upload import upload_dataset

def main():
    print("Fetching papers...")
    papers = fetch_papers()
    
    print("Formatting dataset...")
    formatted = format_dataset(papers)
    save_to_jsonl(formatted)
    
    print("Uploading to Adaption...")
    upload_dataset()
    
    print("Done!")

if __name__ == "__main__":
    main()