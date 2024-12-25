import requests
import boto3
from urllib.parse import urlparse
from os.path import basename
import os
import json
import urllib.parse
from django.conf import settings
import django

  # Replace 'mysite' with your project name

# Now setup Django to load the settings


base_file_path = os.path.join(os.path.dirname(__file__),'..', 'scrapedData', 'scrapedPdfUrls', 'goaPdfUrl.json')
absolute_file_path = os.path.abspath(base_file_path)
AWS_ACCESS_KEY_ID = 'AKIA5G2VGV52YE3X5KAE'
AWS_SECRET_ACCESS_KEY = ''
AWS_STORAGE_BUCKET_NAME = 'launchpad-media'
AWS_S3_REGION_NAME= 'ap-south-1'
try:


    s3 = boto3.client('s3', 
                    aws_access_key_id= AWS_ACCESS_KEY_ID, 
                    aws_secret_access_key= AWS_SECRET_ACCESS_KEY, 
                    region_name= AWS_S3_REGION_NAME)
    print("Successfully created S3 client!")
except Exception as e:
    print(f"Error creating S3 client: {e}")


BUCKET_NAME = AWS_STORAGE_BUCKET_NAME


def encode_metadata_value(value):
    encoded_value = urllib.parse.quote(value)
    return encoded_value

# Function to download PDF from URL and upload to S3
def download_and_upload_pdf(pdf_url, state_name, scheme_url, title):
    try:
        # Download PDF
        response = requests.get(pdf_url, stream=True)
        response.raise_for_status()  # Ensure the request was successful

        # Get the file name from the URL
        file_name = basename(urlparse(pdf_url).path)
        s3_directory = f"pdfs/{state_name}/"
        encoded_title = encode_metadata_value(title)
        metadata = {
            'schemeUrl': scheme_url,
            'title': encoded_title,
            'pdfUrl': pdf_url
        }
        # Upload to S3
        s3.upload_fileobj(response.raw, BUCKET_NAME, f"{s3_directory}{file_name}", ExtraArgs={'ContentType': 'application/pdf', 'Metadata': metadata})
        print(f"Successfully uploaded {file_name} to S3.")
    
    except Exception as e:
        print(f"Error downloading or uploading PDF: {e}")

# Example PDF URLs (replace with actual URLs you have)
pdf_urls = [
    'https://www.goa.gov.in/wp-content/uploads/2024/08/Employment-Subsidy-Scheme-2017.pdf',
    'https://www.goa.gov.in/wp-content/uploads/2024/08/Policy-Goa-Logistics-and-Warehousing-Policy-2023.pdf'
]
# print(absolute_file_path)

with open(absolute_file_path, "r") as file:
    goaData = json.load(file)

# print(goaData)

# Process each PDF URL
for pdf_url in goaData:
    download_and_upload_pdf(pdf_url["pdf_link"],'goa', pdf_url["schemeUrl"], pdf_url["title"])

