# This file is part of the data migration learning project.
# It contains functions for interacting with Google Cloud Storage.

import os
import pandas as pd
import json
import time
import datetime
from google.cloud import storage
from google.cloud.exceptions import NotFound
from pathlib import Path

class CloudStorageManager:
    def __init__(self, bucket_name, project_id):
        self.bucket_name = bucket_name
        self.project_id = project_id
        self.client = storage.Client(project=self.project_id)
        self.bucket = self.client.bucket(self.bucket_name)


    def upload_file(self, local_file_path, cloud_file_name=None):
        if not cloud_file_name:
            cloud_file_name = Path(local_file_path).name
        print(f"Using {cloud_file_name} as the cloud_file_name")

        blob = self.bucket.blob(cloud_file_name)
        
        file_size = os.path.getsize(local_file_path) / (1024*1024)  # Convert to MB
        print(f"File size: {file_size} MB")

        start_time = time.time()

        blob.upload_from_filename(local_file_path)
        upload_time = time.time() - start_time
        print(f" Upload completed in {upload_time:.2f} seconds")
        print(f"File available at: gs://{self.bucket_name}/{cloud_file_name}")

    def download_file(self, cloud_file_name, local_file_path=None):
        blob = self.bucket.blob(cloud_file_name)

        start_time = time.time()
        
        if not blob.exists():
            raise NotFound(f"File {cloud_file_name} not found in bucket {self.bucket_name}")
        
        if not local_file_path:
            local_file_path = "downloads/" + cloud_file_name

        # Create directories if they don't exist
        os.makedirs(os.path.dirname(local_file_path), exist_ok=True)

        original_path = local_file_path
        counter = 1
        while os.path.exists(local_file_path):
            local_file_path = f"{os.path.splitext(original_path)[0]}({counter}){os.path.splitext(original_path)[1]}"
            counter += 1

 
        print(f"Downloading {cloud_file_name} to {local_file_path}...")
        blob.download_to_filename(local_file_path)
        download_time = time.time() - start_time
        print(f"Download completed in {download_time:.2f} seconds")

    def list_files(self, prefix=None, include_details=False):
        """List files in the bucket with an optional prefix."""
        blobs = self.bucket.list_blobs(prefix=prefix)
        file_list = []
        for blob in blobs:
            if include_details:
                file_info = {
                    'name': blob.name,
                    'size_bytes': blob.size,
                    'size_mb': blob.size / (1024 * 1024),  # Convert to MB
                    'uploaded': blob.time_created,
                    'type': blob.content_type
                }
                file_list.append(file_info)
            else: file_list.append(blob.name)
        return file_list

    def simulate_migration(self, local_folder_path):
        all_files = []
        for root, dirs, files in os.walk(local_folder_path):
            for filename in files:
                full_local_path = os.path.join(root, filename)
                relative_path = os.path.relpath(full_local_path, local_folder_path)
                all_files.append((full_local_path, relative_path))

        total_files = len(all_files)
        success_count = 0
        failure_count = 0

        for i, (local_path, cloud_name) in enumerate(all_files, 1):
            print(f"Processing file {i} of {total_files}: {cloud_name}")
            try: 
                self.upload_file(local_path, cloud_name)
                success_count += 1
            except Exception as e:
                print(f"Failed to upload {cloud_name}: {e}")
                failure_count += 1

        print(f"Migration completed: {success_count} successful, {failure_count} failed out of {total_files} files.")

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    bucket_name = os.getenv('GCS_BUCKET_NAME')
    project_id = os.getenv('GCP_PROJECT_ID')

    print(f"Using bucket: {bucket_name}")
    print(f"Using project: {project_id}")
          
    manager = CloudStorageManager(bucket_name, project_id)
    
    action = input("Enter 'u' for upload, 'd' for download, 'l' for list, or 'm' for migration: ").lower()
    if action == 'u':
        manager.upload_file('data/email_sample_100.csv')
    elif action == 'd':
        manager.download_file('email_sample_100.csv')
    elif action == 'l':
        files = manager.list_files(include_details=True)
        print(f"Found {len(files)} files:")
        for file in files:
            print(f"{file['name']} {file['size_mb']:.2f} MB")
    elif action == 'm':
        manager.simulate_migration('data')