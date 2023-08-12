from dotenv import load_dotenv
import os
import csv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Access the spreadsheet
data_path = os.getenv("DATA_PATH")

if not data_path:
    print("Valid data path not found in .env file")

# Read the spreadsheet
connections = []
with open(data_path, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    connections = [row for row in csv_reader]
    if 'First Name' not in connections[0]:
           print('Ensure that column titles are in first row of spreadsheet!')
           os._exit(1)

# Helper functions
def does_company_match(input, company):
    if input.lower() == company.lower() or \
        input.lower() == company.lower().split(' ')[0]:
        return True
    return False

def does_position_match(keywords, role):
    keywords_arr = keywords.lower().split(' ')
    for word in role.lower().split(' '):
        if word in keywords_arr:
            return True
    return False

def days_connected(date):
    date_style = '%d %b %Y' # Format used by LinkedIn
    return (datetime.now() - datetime.strptime(date, date_style)).days

def filter_connections(company=None, position=None, days=None):
    filtered_connections = []
    
    for connection in connections:
        if (not company or does_company_match(company, connection['Company'])) and \
           (not position or does_position_match(position, connection['Position'])) and \
           (not days or days_connected(connection['Connected On']) >= int(days)):
            filtered_connections.append(connection)
    
    return filtered_connections

# Main
def main():
    company = input('Enter company name (leave empty for any): ')
    position = input('Enter position keywords (leave empty for any): ')
    days = input('Enter minimum days ago connected (leave empty for any): ')
    
    filtered_connections = filter_connections(company, position, days)
    
    if not filtered_connections:
        print('No connections match the criteria.')
       
    else:
        print(f'Found {len(filtered_connections)} connections matching your criteria:')
        for connection in filtered_connections:
            print('-', f'{connection["First Name"]} {connection["Last Name"]} ({connection["Position"]} @{connection["Company"]}): {connection["URL"]}')

if __name__ == '__main__':
    main()