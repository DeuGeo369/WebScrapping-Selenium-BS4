import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# --- CONFIGURATION ---
CHROMEDRIVER_PATH = r'F:\HCJS\Webscrapping\drivers\chromedriver.exe'
URL = #Find your own URL
EXISTING_FILE = 'incident.xlsx'
OUTPUT_FILE = 'incident_report_new_only.csv'

# --- Load and Normalize Existing Data ---
existing_df = pd.read_excel(EXISTING_FILE)
existing_normalized = existing_df.astype(str).apply(lambda col: col.str.strip().str.lower())

# Flatten columns if multi-level and match column names based on key substrings
column_map = {}
for key in ['district', 'incident date', 'total death', 'incident place']:
    for col in existing_df.columns:
        col_name = ' '.join(col).lower() if isinstance(col, tuple) else col.lower()
        if key in col_name:
            column_map[key] = col
            break

if len(column_map) < 4:
    raise KeyError(" Could not find all required columns. Found: " + str(column_map))

# Use the actual mapped column names
KEY_COLUMNS = list(column_map.values())

# Normalize existing data keys
existing_keys = existing_normalized[KEY_COLUMNS].apply(lambda row: '|'.join(row), axis=1).tolist()

# --- Setup Selenium Headless Browser ---
options = Options()
options.add_argument("--headless")
service = Service(executable_path=CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)
driver.get(URL)
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#replaceTable table")))

# --- Scraping ---
all_rows = []
seen_keys = set()
match_count = 0

while match_count < 3:
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table = soup.select_one('#replaceTable table')

    headers = [th.text.strip() for th in table.select('thead th')]
    for tr in table.select('tbody tr'):
        cells = [td.text.strip() for td in tr.find_all('td')]
        if not cells:
            continue

        row_dict = dict(zip(headers, cells))
        normalized_row = pd.Series(row_dict).astype(str).str.strip().str.lower()
        key = '|'.join([normalized_row.get(col, '') for col in KEY_COLUMNS])

        if key in existing_keys:
            match_count += 1
            print(f"Matched existing record {match_count}: {key}")
            if match_count >= 3:
                break
        elif key not in seen_keys:
            all_rows.append(cells)
            seen_keys.add(key)

    if match_count >= 3:
        print(" Found 3 existing matches. Scraping stopped.")
        break

    try:
        next_button = driver.find_element(By.LINK_TEXT, '>>')
        next_button.click()
        time.sleep(2)
    except Exception as e:
        print(" No more pages or navigation error:", str(e))
        break

driver.quit()

# --- Prepare Output DataFrame ---
expected_columns = [
    'District', 'VDC/Municipality', 'Ward No.', 'Incident Place', 'Incident Date', 'Incident',
    'Death Male', 'Death Female', 'Death Unknown', 'Total Death', 'Missing People',
    'Affected Family', 'Estimated Loss', 'Injured',
    'Govt. Houses Fully Damaged', 'Govt. Houses Partially Damaged',
    'Private House Fully Damaged', 'Private House Partially Damaged',
    'Displaced Male(N/A)', 'Displaced Female(N/A)', 'Property Loss',
    'No. of Displaced Family', 'Cattles Loss', 'Displaced Shed', 'Source', 'Remarks'
]

new_data_df = pd.DataFrame(all_rows, columns=headers)

# Rename 'Local Level' column to 'VDC/Municipality'
new_data_df.rename(columns={"Local Level": "VDC/Municipality"}, inplace=True)
new_data_df.rename(columns={"Office": "Source"}, inplace=True)


# Normalize and reorder to expected columns
normalized_header_map = {col.strip().lower(): col for col in new_data_df.columns}
final_columns = [normalized_header_map.get(col.lower(), col) for col in expected_columns]
new_data_df = new_data_df.reindex(columns=final_columns).fillna('')

# Save new records to CSV
new_data_df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
print(f" {len(new_data_df)} new records saved to '{OUTPUT_FILE}'.")

# --- Prepend new rows to Excel ---
if not new_data_df.empty:
    # Reindex to match structure of existing file
    for col in expected_columns:
        if col not in existing_df.columns:
            existing_df[col] = ''  # Add missing columns if any

    # Ensure new_data_df has the same columns and order
    existing_df = existing_df[expected_columns]
    new_data_df = new_data_df[expected_columns]

    combined_df = pd.concat([new_data_df, existing_df], ignore_index=True)

    # Save back to Excel
    combined_df.to_excel(EXISTING_FILE, index=False)
    print(f" Prepended {len(new_data_df)} rows to '{EXISTING_FILE}'.")
else:
    print("ℹ No new data found to prepend.")

