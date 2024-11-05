from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import sqlite3

# Set up the web driver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

driver.get('https://www.pensford.com/resources/forward-curve')

# Wait for the table to be fully loaded
table_loaded = False
while not table_loaded:
    try:
        table = driver.find_element(By.ID, 'curvetable')
        table_loaded = True
    except:
        time.sleep(1)


# Function to clean and format dates
def clean_date(date_str):
    try:
        # Split the date into components
        month, day, year = date_str.split("/")

        # Add leading zeros if necessary
        month = month.zfill(2)  # Ensures month is two digits
        day = day.zfill(2)  # Ensures day is two digits

        # Reformat to YYYY-MM-DD
        formatted_date = f"{year}-{month}-{day}"

        return formatted_date  # Return the formatted date

    except ValueError:
        # If parsing fails, log and return None
        print(f"Invalid date format: {date_str}")
        return None


# Extract the 1-month forward rates
forward_rates = []
rows = table.find_elements(By.TAG_NAME, 'tr')
for row in rows[1:]:
    cells = row.find_elements(By.TAG_NAME, 'td')
    if len(cells) >= 2:
        date_str1 = cells[0].text.strip()
        rate_str = cells[1].text.strip()
        rate_str = rate_str.replace('%', '')
        forward_rates.append((clean_date(date_str1), float(rate_str)))

# Print the 1-month forward rates
print(forward_rates)

# Step 3: Set up SQLite database and table
conn = sqlite3.connect("forward_rates.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS ForwardCurve (
        ResetDate TEXT,
        OneMonthSOFR TEXT
    )
''')

#Step 4: Prevent Multiple Runs
cursor.execute("DELETE FROM ForwardCurve;")
conn.commit()

# Step 5: Insert data into the database
cursor.executemany('''
    INSERT INTO ForwardCurve (ResetDate, OneMonthSOFR) 
    VALUES (?, ?)
''', forward_rates)

conn.commit()
conn.close()

# Close the web driver
driver.quit()
