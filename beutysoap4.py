import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the incident report page
url = 'http://drrportal.gov.np/'

# Send an HTTP GET request to the page
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}
response = requests.get(url, headers=headers)
response.raise_for_status()

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Locate the incident table
table = soup.select_one('#replaceTable table')

# Extract table headers
headers = [th.text.strip() for th in table.select('thead th')]

# Extract table rows
rows = []
for tr in table.select('tbody tr'):
    cells = [td.text.strip() for td in tr.find_all('td')]
    if cells:
        rows.append(cells)

# Convert to DataFrame
df = pd.DataFrame(rows, columns=headers)

# Display or save
# print(df.head())
df.to_csv('incident_report.csv', index=False)


#Unfortunately, requests and BeautifulSoup don't interact with JavaScript, which is why you're seeing only the initial page.

# S.No.,District,Local Level,Incident,Incident Date,Death Male,Death Female,Death Unknown,Total Death,Missing People,Affected Family,Estimated Loss,Injured,Govt. Houses Fully Damaged,Govt. Houses Partially Damaged,Private House Fully Damaged,Private House Partially Damaged,Displaced Male(N/A),Displaced Female(N/A),Property Loss,Incident Place,Damaged Houses(%),No. of Displaced Family,Cattles Loss,Displaced Shed,Office,Remarks
# 1,Okhaldhunga,Chishankhugadhi Rural Municipality,Fire,2025-05-14,0,0,0,0,0,1,,0,0,0,1,0,0,0,0,Bogatichhap,0,0,0,0,Nepal Police,Kaji Bahadur Thapa
# 2,Morang,Letang Municipality,Fire,2025-05-14,0,0,0,0,0,2,2500000,0,0,0,0,0,0,0,0,,0,0,0,0,Nepal Police,Dilli Pokhrel
# 3,Kathmandu,Kathmandu Metropolitan City,Fire,2025-05-14,0,0,0,1,0,4,,1,0,0,0,0,0,0,0,Makhan Galli,0,0,0,0,Nepal Police,Dayaram Shrestha/Rukesh Shrestha / Hiumaya Kisan (Injured)
# 4,Dhanusha,Janakpur Submetropolitan City,Fire,2025-05-13,0,0,0,0,0,1,300000,0,0,0,0,0,0,0,0,Musartole,0,0,0,0,Nepal Police,Aklesh Kumar Chaudhary
# 5,Chitawan,Bharatpur Metropolitan City,Wind storm,2025-05-13,0,0,0,0,0,1,80000,0,0,0,0,1,0,0,0,,0,0,0,0,Nepal Police,Chandra Baral
# 6,Tanahu,Aanbookhaireni Rural Municipality,Thunderbolt,2025-05-13,0,0,0,0,0,3,,3,0,0,0,0,0,0,0,,0,0,0,0,Nepal Police,Sar Bahadur Gurung/Purna Bahadur Gurung/Sangita Gurung
# 7,Sunsari,Barahkshetra Municipality,Fire,2025-05-13,0,0,0,0,0,1,200000,0,0,0,0,0,0,0,0,Bishalchowk,0,0,0,1,Nepal Police,Bhakta Bahadur Karki
# 8,Lalitpur,Lalitpur Metropolitan City,Fire,2025-05-13,0,0,0,0,0,3,,1,0,0,0,0,0,0,0,Harisiddhi,0,0,0,0,Nepal Police,Sanu Chaudhary
# 9,Morang,Rangeli Municipality,Wind storm,2025-05-13,0,0,0,0,0,1,50000,0,0,0,0,0,0,0,0,,0,0,0,0,Nepal Police,Jogindra Mandal
# 10,Chitawan,Kalika Municipality,Wind storm,2025-05-13,0,0,0,0,0,1,,1,0,0,0,0,0,0,0,,0,0,0,0,Nepal Police,Aayush Gurung
