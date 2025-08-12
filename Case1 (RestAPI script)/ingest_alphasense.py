import requests

# Replace these variables with your actual values
API_URL = "https://research.alpha-sense.com/services/i/ingestion-api/v1/upload-document"
BEARER_TOKEN = "your_bearer_token"
CLIENT_ID = "enterprise-sync"
DOCUMENT_PATH = "/document.txt"  # Path to your document
ATTACHMENT_PATHS = [
    "/path/to/20221020 - EnterpriseSync - TSLA - Doc - 1 page.pdf",  # Attachments
    "/path/to/20230201 - Onenote - Demo Page 2 - 1 page.pdf"
]
METADATA = {
    "title": "Document Upload",
    "companies": [{
        "value": "US5949181045",
        "operation": "ADD",
        "identifier": "ISIN",
        "salience": "PRIMARY"
    }],
    "customTags": [
        {
            "name": "pb_tag",
            "visibility": "PUBLIC",
            "operation": "ADD"
        },
        {
            "name": "pV_tag",
            "visibility": "PRIVATE",
            "operation": "ADD"
        }
    ],
    "shareInfo": {
        "mode": "DEFAULT"
    },
    "docAuthors": [{
        "authorName": "Author1",
        "operation": "ADD"
    }],
    "documentOwner": "username",  # Replace with the actual document owner
    "createdTimestamp": "yyyy-mm-ddThh:mm:ssZ",  # Replace with the actual timestamp
    "sourceType": "Internal Research",
    "documentUrl": "https://www.example.com"
}

# Prepare headers and files
headers = {
    'Authorization': f'bearer {BEARER_TOKEN}',
    'clientId': CLIENT_ID
}

files = {
    'file': open(DOCUMENT_PATH, 'rb')  # Open the document to upload
}

# Add attachments to the request
for attachment_path in ATTACHMENT_PATHS:
    files[f'attachments'] = open(attachment_path, 'rb')

# Add metadata as a string
metadata = str(METADATA)

# Prepare the payload for the POST request
payload = {
    'metadata': metadata
}

# Send the request
try:
    response = requests.post(API_URL, headers=headers, files=files, data=payload)

    # Check for successful response
    if response.status_code == 200:
        print("Document uploaded successfully.")
    
    # Handle specific error codes
    elif response.status_code == 400:
        print("Bad Request: The server could not understand the request. Please check the input data and try again.")
        print(f"Error details: {response.text}")
    
    elif response.status_code == 404:
        print("Not Found: The requested resource could not be found. Please check the API URL or the document ID.")
        print(f"Error details: {response.text}")
    
    elif response.status_code == 500:
        print("Server Error: There was a problem with the server. Please try again later.")
        print(f"Error details: {response.text}")
    
    # Handle other status codes
    else:
        print(f"Failed to upload document: {response.status_code}")
        print(response.text)

except requests.exceptions.RequestException as e:
    # Catch network-related errors or request timeouts
    print(f"An error occurred while sending the request: {e}")

finally:
    # Close file handlers to ensure no file is left open
    files['file'].close()
    for attachment_path in ATTACHMENT_PATHS:
        files[attachment_path].close()
