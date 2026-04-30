import os
import time
import httpx
import httpx._api
from adaption import Adaption
from config import ADAPTION_API_KEY

# Monkey patch httpx.put to always use a long timeout
_original_put = httpx.put
def _patched_put(url, **kwargs):
    kwargs.setdefault("timeout", 600.0)
    return _original_put(url, **kwargs)
httpx.put = _patched_put
httpx._api.put = _patched_put

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