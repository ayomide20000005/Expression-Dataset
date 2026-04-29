import os
import time
from adaption import Adaption
from config import ADAPTION_API_KEY

client = Adaption(api_key=ADAPTION_API_KEY)

def upload_dataset(filepath="dataset.jsonl"):
    print("Uploading dataset to Adaption...")
    upload = client.datasets.upload_file(filepath)
    
    print("Waiting for processing...")
    while True:
        status = client.datasets.get_status(upload.dataset_id)
        if status.row_count is not None:
            break
        time.sleep(2)
    
    print("Running adaptation...")
    job = client.datasets.run(
        upload.dataset_id,
        column_mapping={"prompt": "input"},
        job_specification={"max_rows": 1000},
    )
    
    print(f"Launched! Estimated time: ~{job.estimated_minutes} mins")
    client.datasets.wait_for_completion(upload.dataset_id, timeout=3600)
    
    dataset = client.datasets.get(upload.dataset_id)
    if dataset.evaluation_summary:
        print(f"Quality: {dataset.evaluation_summary.grade_before} → {dataset.evaluation_summary.grade_after}")
    
    url = client.datasets.download(upload.dataset_id)
    print(f"Download your dataset here: {url}")