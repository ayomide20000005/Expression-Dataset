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
    
    print(f"✅ Dataset uploaded successfully!")
    print(f"Dataset ID: {upload.dataset_id}")
    print("Now go to the Adaption platform to run the adaptation!")