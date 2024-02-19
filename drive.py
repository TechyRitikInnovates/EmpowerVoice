from flask import Flask, render_template, request, jsonify
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload
import os
import time

app = Flask(__name__)

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'service_account.json'
PARENT_FOLDER_ID = "1JqubTwwfcgv3sANDKn6dROQaf8uGXzXy"
DOWNLOAD_FOLDER = "downloads/"

def authenticate():
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return creds

def download_files():
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)
    results = service.files().list(q="'{}' in parents".format(PARENT_FOLDER_ID), fields="files(id, name)").execute()
    files = results.get('files', [])
    if not files:
        print('No new files found.')
    else:
        for file in files:
            file_id = file['id']
            file_name = file['name']
            file_path = os.path.join(DOWNLOAD_FOLDER, file_name)
            if not os.path.exists(file_path):
                request = service.files().get_media(fileId=file_id)
                fh = open(file_path, "wb")
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                print("Downloaded", file_name)

def main():
    if not os.path.exists(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)
        
    while True:
        download_files()
        time.sleep(1)  # Check for new files every 60 seconds

if __name__ == "__main__":
    app.run(debug=True, port=5000)
    main()
