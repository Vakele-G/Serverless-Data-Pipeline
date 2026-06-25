import requests
import json

api_url = "https://sd3frh2wa8.execute-api.af-south-1.amazonaws.com/dev/submit-report"

# The structured CSV text your cleaner actually expects
messy_csv_data = """location, issueType, urgency
  Cape Town Main Road  ,   water_leak   ,  high  
  Bellville  , pothole , medium"""

data = {
    "raw_csv": messy_csv_data
}

response = requests.post(api_url, json=data)
print(f"Status code: {response.status_code}")