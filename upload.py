import os
import time
import httpx
from adaption import Adaption
from config import ADAPTION_API_KEY

os.environ["HTTPX_TIMEOUT"] = "300"

httpx._config.DEFAULT_TIMEOUT_CONFIG = httpx.Timeout(300.0)

client = Adaption(api_key=ADAPTION_API_KEY)

def upload_dataset(filepath="dataset.jsonl"):
    print("Uploading dataset to Adaption...")

    with httpx.Client(timeout=300.0) as http:
        file_bytes = open(filepath, "rb").read()
        print(f"Dataset size: {len(file_bytes) / 1024:.1f} KB")

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