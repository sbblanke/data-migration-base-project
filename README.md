# Data Migration Base Project

A Python-based cloud storage migration simulation tool built for learning enterprise data archival strategies and cloud storage management.

## Overview

This project demonstrates building a comprehensive cloud storage management system using Google Cloud Storage APIs. It was developed as part of a learning journey to understand cloud migration concepts and enterprise data archival strategies.

## Features

### Core Functionality

- **File Upload**: Upload individual files or entire directories to Google Cloud Storage
- **File Download**: Download files with automatic duplicate handling (Windows-style naming)
- **File Listing**: List bucket contents with detailed metadata (size, upload date, content type)
- **Migration Simulation**: Batch process entire directories with progress tracking and error handling

### Key Capabilities

- **Recursive Directory Processing**: Preserves folder structure during migration
- **Error Resilience**: Continues processing even if individual files fail
- **Progress Tracking**: Real-time feedback during batch operations
- **Format Support**: Handles multiple file formats (CSV, compressed files, Parquet)
- **Smart Path Handling**: Automatic directory creation and duplicate file management

## Technical Implementation

### Architecture

- **Object-Oriented Design**: Clean `CloudStorageManager` class with focused methods
- **Google Cloud Integration**: Direct API integration using `google-cloud-storage` library
- **Error Handling**: Robust exception handling for network and file system operations
- **Performance Monitoring**: Built-in timing for upload/download operations

### File Structure

```
data_migration_learning/
├── src/
│   └── cloud_storage.py       # Main application
├── credentials/               # GCS Credentials (not tracked)
├── data/                      # Data files to be migrated (not tracked)
├── downloads/                 # Data files pulled from storage (not tracked)
├── .env                       # Environment variables (not tracked)
├── requirements.txt           # Python dependencies
└── README.md                 # This file
```

## Setup Instructions

### Prerequisites

- Python 3.12+
- Google Cloud Platform account
- Google Cloud Storage bucket

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/sbblanke/data-migration-base-project.git
   cd data-migration-base-project
   ```

2. **Set up virtual environment**

   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # or
   source venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Google Cloud credentials**

   - Create a service account in Google Cloud Console (https://console.cloud.google.com/)
   - Download the JSON key file to `credentials/`
   - Set the environment variable: `GOOGLE_APPLICATION_CREDENTIALS=credentials/your-key.json`

5. **Set up environment variables**
   Create a `.env` file:
   ```
   GCS_BUCKET_NAME=your-bucket-name
   GCP_PROJECT_ID=your-project-id
   GOOGLE_APPLICATION_CREDENTIALS=credentials/your-service-account-key.json
   ```

## Usage

### Interactive Mode

```bash
python src/cloud_storage.py
```

Choose from:

- **Upload** (`u`): Upload a single file
- **Download** (`d`): Download a file from cloud storage
- **List** (`l`): View all files in the bucket with metadata
- **Migration** (`m`): Simulate full directory migration

### Example Output

```
Using bucket: {bucket name}}
Using project: {project name}
Enter 'u' for upload, 'd' for download, 'l' for list, or 'm' for migration: m

Processing file 1 of 5: email_sample_100.csv
File size: 0.07 MB
Upload completed in 0.84 seconds

Processing file 2 of 5: migration_test_1000.csv
File size: 0.66 MB
Upload completed in 0.74 seconds

Migration completed: 5 successful, 0 failed out of 5 files.
```

## Learning Outcomes

This project demonstrates understanding of:

### Technical Skills

- **Cloud Storage APIs**: Direct integration with Google Cloud Storage
- **Python Development**: Object-oriented programming, file handling, error management
- **Batch Processing**: Large-scale data migration workflows
- **Performance Optimization**: Timing analysis and format comparison

### Business Applications

- **Enterprise Data Archival**: Cost-effective strategies for reducing storage expenses
- **Compliance Considerations**: Data retention and privacy law implications
- **Migration Planning**: Risk assessment and workflow design

## Real-World Application

This learning project directly applies to enterprise scenarios where organizations need to:

- Migrate data from expensive platforms (like Salesforce) to cost-effective cloud storage
- Implement automated archival strategies
- Maintain data accessibility while reducing storage costs
- Ensure compliance with data retention requirements

## Dependencies

```
google-cloud-storage>=2.10.0
pandas>=2.0.0
python-dotenv>=1.0.0
pyarrow>=13.0.0
faker>=19.0.0
```

## Security Notes

- Never commit credentials or API keys to version control
- Use environment variables for sensitive configuration
- Implement proper access controls on cloud storage buckets
- Consider encryption for sensitive data

## Future Enhancements

Potential improvements for production use:

- Integration with business intelligence tools (Tableau, Power BI)
- Advanced filtering and search capabilities
- Automated retention policy enforcement
- Cost monitoring and alerting
- Multi-cloud support (AWS S3, Azure Blob Storage)

---

_This project was developed as part of a Python learning journey focused on solving real-world business challenges in enterprise data management._
