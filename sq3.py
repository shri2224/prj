import pandas as pd
import re

# Load CSV file
input_csv = 'incident_export_20_11_2025_08_32_47.csv'  # Change as needed
df = pd.read_csv(input_csv)

def parse_description(desc):
    result = {}
    desc = str(desc)
    # Extract Title (Event Name)
    m = re.search(r'Event Name:\s*(.+?)(?:\n|$)', desc)
    result['Title'] = m.group(1).strip() if m else None
    # Host IP
    m = re.search(r'Host IP:\s*(.+?)(?:\n|$)', desc)
    result['Host_IP'] = m.group(1).strip() if m else None
    # Host Name
    m = re.search(r'Host Name:\s*(.+?)(?:\n|$)', desc)
    result['Host_Name'] = m.group(1).strip() if m else None
    # Event Time
    m = re.search(r'Event Time:\s*(.+?)(?:\n|$)', desc)
    result['Event_Time'] = m.group(1).strip() if m else None
    # Event URL and Location extraction
    m = re.search(r'Event URL:\s*(.+?)(?:\n|$)', desc)
    url = m.group(1).strip() if m else ""
    # Use regex to extract location code between 'https://' and '-iopex'
    loc_match = re.search(r'https://(.*?)-iopex', url)
    result['Location'] = loc_match.group(1) if loc_match else None
    return result

parsed = df['description'].apply(parse_description)
parsed_df = pd.DataFrame(parsed.tolist())

result_df = pd.DataFrame({
    'ID': df['id'],
    'Title': parsed_df['Title'],
    'Host_IP': parsed_df['Host_IP'],
    'Host_Name': parsed_df['Host_Name'],
    'Event_Time': parsed_df['Event_Time'],
    'Location': parsed_df['Location']
})

# Filtering by downtime/unavailable keywords in Title
keywords = ['not available', 'unavailable', 'down']
pattern = '|'.join(keywords)
filtered_df = result_df[result_df['Title'].str.lower().str.contains(pattern, na=False)]

filtered_df.to_csv('AP2.csv', index=False)

print("Filtered CSV with Location column saved as server_title_down_incidents.csv")
print(filtered_df.head())
