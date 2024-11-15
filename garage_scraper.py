import requests 
import csv

# URL of the UCF Garage Counter API (this URL could be found in the network traffic)
api_url = "https://secure.parking.ucf.edu/GarageCounter/GetOccupancy"

# Make a GET request to the API
response = requests.get(api_url)
event_type = 'club_meeting'
excel_response = 'Garage A' # GARAGE FROM CSV

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    
    # Open CSV file to write the data
    with open('garage_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Write the header row
        writer.writerow(["Garage", "Available", "Total", "Percent Full"])

        # Iterate through the data and extract relevant information
        for item in data:
            if 'location' in item and 'counts' in item['location'] and item['location']['name'] == excel_response:
                location = item['location']['name']
                available = item['location']['counts']['available']
                total = item['location']['counts']['total']
                percent_full = round((total - available) / total * 100, 2) if total > 0 else 100
                # Write data row to CSV
                writer.writerow([location, available, total, f"{percent_full}%"])

    print("Garage data has been saved to 'garage_data.csv'.")
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")