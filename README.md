# WebScrapping-Selenium-BS4
# Incident Report Web Scraping & Data Processing

This project scrapes incident reports from the a portal, processes the data, and integrates it with existing records in Excel. The script extracts details like incident date, district, total deaths, damages, and other related information. It also identifies and appends any new records that are not already present in the existing dataset.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Script Workflow](#script-workflow)
- [Configuration](#configuration)
- [Expected Output](#expected-output)

## Prerequisites

Before running the script, ensure you have the following installed on your system:

- Python 3.x+
- Libraries:
  - `pandas`
  - `selenium`
  - `beautifulsoup4`
  - `openpyxl` (for reading and writing Excel files)

Additionally, you need a compatible version of [Chrome WebDriver](https://sites.google.com/a/chromium.org/chromedriver/) for Selenium to work.

## Installation

1. Install the required libraries via pip:
   ```bash
   pip install pandas selenium beautifulsoup4 openpyxl

## Configuration

1. **Download Chrome WebDriver**  
   Download the appropriate version of [Chrome WebDriver](https://sites.google.com/a/chromium.org/chromedriver/) for your operating system and place it in the specified `CHROMEDRIVER_PATH`.

2. **Modify the Configuration in the Script**  
   Open the script and modify the configuration section to set the following paths and URL:

    - **CHROMEDRIVER_PATH**: The local path where your `chromedriver.exe` is located.
    - **URL**: The webpage URL you wish to scrape (defaults to `http://drrportal.gov.np/`).
    - **EXISTING_FILE**: Path to the existing Excel file where incident reports are stored (e.g., `incident.xlsx`).
    - **OUTPUT_FILE**: Path to save new records as a CSV file (e.g., `incident_report_new_only.csv`).

### Running the Script:
After configuring the script, run it using the following command:


python scraper.py

### Script Workflow:
- The script opens a headless browser using Selenium to scrape data from the DRR Portal.
- It waits for the relevant table to load and extracts rows of incident data.
- Each row is normalized and checked against existing records in the provided Excel file.
- If the record does not exist in the Excel file, it is added to a new CSV file.
- Once 3 matching records are found, scraping stops.
- The new records are prepended to the existing Excel file.
## Usage
## Configuration
In the script, make sure to set the following values to match your environment:

- **CHROMEDRIVER_PATH**: Path to your ChromeDriver.
- **URL**: The webpage URL you wish to scrape (defaults to DRR Portal).
- **EXISTING_FILE**: Path to the Excel file that contains the existing incident reports.
- **OUTPUT_FILE**: Path to the CSV file to save new records.

## Expected Output

- **CSV File (`incident_report_new_only.csv`)**: This file will contain new records that were scraped and not already present in the existing dataset.
  
- **Excel File (`incident.xlsx`)**: The new records will be prepended to this Excel file.

### Example Output:
```bash
✅ 50 new records saved to 'incident_report_new_only.csv'.
📌 Prepended 50 rows to 'incident.xlsx'.
