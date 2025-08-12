# AlphaSense Document Upload Script - Explanation

## Overview

This Python script allows users to upload documents and attachments to the AlphaSense platform using their Ingestion API. The script uploads a document file, attaches additional files (PDFs), and includes metadata for categorization. It also includes error handling to manage different HTTP response codes (e.g., 400, 404, 500), ensuring robustness and reliability during document upload processes.

## What Was Implemented

### Functionality:
- **Document Upload**: The script uploads a document and associated attachments to the AlphaSense platform via their `POST /upload-document` API endpoint.
- **Metadata**: The script includes metadata in the request, such as document title, company identifiers (ISIN), custom tags, document owner, and other document-related information.
- **Attachments**: In addition to the main document, additional PDF files are attached to the request, which is a common scenario when uploading documents for review or categorization.
- **Error Handling**: 
  - The script checks the HTTP response codes and provides specific feedback for common errors (400, 404, 500) and prints the corresponding error messages for easy troubleshooting.
  - It also handles network-related issues like connection problems, timeouts, or invalid requests.

### How to Run It

1. **Pre-requisites**:
   - Ensure Python 3.x is installed.
   - Install the `requests` library to handle HTTP requests:
     ```bash
     pip install requests
     ```

2. **Configuration**:
   - Replace the placeholders in the script:
     - `BEARER_TOKEN`: Your AlphaSense authentication token.
     - `CLIENT_ID`: The client ID associated with your account.
     - `DOCUMENT_PATH`: The local path to the document file you want to upload.
     - `ATTACHMENT_PATHS`: Paths to any PDF attachments you wish to include.
     - `METADATA`: Customize the metadata (e.g., document title, company identifiers, etc.) as required.
   
3. **Running the Script**:
   - Open your terminal and navigate to the directory where the script is located.
   - Run the script using Python:
     ```bash
     python upload_document.py
     ```

4. **Output**:
   - If the upload is successful, you will see:
     ```bash
     Document uploaded successfully.
     ```
   - If an error occurs (e.g., bad request, file not found, server error), the script will display a corresponding error message to guide troubleshooting.

## Improvements & Full Pipeline Considerations

### Improvements:
- **Error Handling & Retries**: 
  - For a more robust pipeline, you can implement retry logic (e.g., using exponential backoff) for transient errors such as timeouts or 500 server errors.
  - Expand the script to handle more HTTP status codes (e.g., 401 for authentication errors, 403 for authorization issues).
  
- **Batch Processing**: 
  - The script can be extended to handle multiple document uploads in a batch, especially useful for large volumes of data. You can loop through a list of files and upload them sequentially or in parallel.

- **Configuration Management**: 
  - Store configuration values (API key, file paths, etc.) in an external configuration file or environment variables for better security and flexibility in production environments.

- **Logging**: 
  - Add logging functionality (e.g., using Python’s `logging` module) to keep track of script execution, error details, and document upload success/failure for better monitoring and debugging.

- **Scheduled Jobs**: 
  - Set up cron jobs (for Linux/macOS) or Task Scheduler (for Windows) to automate the document upload process on a daily or hourly basis.

### Important Considerations for a Full Pipeline:
- **API Rate Limiting**: Ensure that your pipeline respects any rate limits imposed by the AlphaSense API (e.g., maximum number of requests per minute or hour). Implement backoff and retry strategies to avoid hitting these limits.
- **Scalability**: Consider scaling the script for handling thousands of documents by incorporating batch processing, parallel uploads, and error management.
- **Security**: Ensure that API keys and sensitive information are never hardcoded into the script. Use environment variables or encrypted secrets management systems to handle credentials.
  
## Required Configuration

1. **API Key**: 
   - Replace `BEARER_TOKEN` with your valid AlphaSense bearer token for authentication. You can obtain this token from your AlphaSense account.
   
2. **Client ID**:
   - Replace `CLIENT_ID` with your specific client identifier (`enterprise-sync` or another provided by AlphaSense).
   
3. **File Paths**:
   - Set the correct file paths for the document you want to upload (`DOCUMENT_PATH`) and any attachments (`ATTACHMENT_PATHS`). These files must exist on the local file system and should be accessible by the script.
   
4. **Metadata**:
   - The metadata section of the script should be customized according to your use case. Adjust fields like `title`, `companies`, `customTags`, `docAuthors`, and others to match the document’s attributes you want to track in AlphaSense.

5. **File Extensions**:
   - Ensure that the documents you are uploading have supported file extensions (PDF, DOCX, TXT, etc.) as outlined in the API documentation. If uploading unsupported file types, the API will return an error.

## Conclusion

This script provides a straightforward solution for uploading documents to AlphaSense with attachments and metadata. It’s ideal for testing purposes and can be extended into a full automation pipeline with error handling, scheduling, and batch processing for production use. By making improvements such as retry mechanisms, logging, and scalability considerations, you can transform this simple script into a robust, enterprise-level document ingestion pipeline.
