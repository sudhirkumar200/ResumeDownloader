import csv
import requests
from pathlib import Path

def download_file(url, directory):
    # Check if the URL is a Google Drive shared link and convert it to a direct download link
    if 'drive.google.com' in url and '/file/d/' in url:
        file_id = url.split('/file/d/')[1].split('/')[0]
        url = f'https://drive.google.com/uc?export=download&id={file_id}'
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        
        # Extract a valid filename from the Content-Disposition header if available
        content_disposition = response.headers.get('content-disposition')
        if content_disposition:
            filename = content_disposition.split('filename=')[1].strip('"')
        else:
            filename = url.split('/')[-1]
        
        # Ensure filename is filesystem-safe
        filename = "".join(i for i in filename if i not in "\/:*?<>|")
        
        filepath = Path(directory) / filename
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {filename}")
    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error: {err}")
    except requests.exceptions.RequestException as err:
        print(f"Error: {err}")


# Replace 'your_csv_file.csv' with the path to your CSV file
csv_file = 'your_csv_file.csv'
# Replace 'download_directory' with the path to the directory where you want to save the PDFs
download_directory = 'download_directory'

# Ensure the download directory exists
Path(download_directory).mkdir(parents=True, exist_ok=True)

# Read the CSV file and download the PDFs
with open(csv_file, newline='') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        pdf_url = row[0]  # Assuming the PDF URL is in the first column
        download_file(pdf_url, download_directory)