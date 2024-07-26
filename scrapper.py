import requests
import pandas as pd
import os
from image_handler import save_image, delete_images
from ai_integration import generate_report
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define your API key and Custom Search Engine ID
API_KEY = os.getenv('API_KEY')
SEARCH_ENGINE_ID = os.getenv('SEARCH_ENGINE_ID')

def google_search(query, num_results=10, include_images=False, site_filter=None):
    search_url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        'key': API_KEY,
        'cx': SEARCH_ENGINE_ID,
        'q': query,
        'num': min(num_results, 30)  # Ensure num_results does not exceed 30
    }
    if include_images:
        params['searchType'] = 'image'
    if site_filter:
        params['q'] += f" site:{site_filter}"
    
    response = requests.get(search_url, params=params)
    response.raise_for_status()
    return response.json()

def parse_results(results, include_images=False):
    items = results.get('items', [])
    data = []
    for item in items:
        entry = {
            'title': item.get('title'),
            'link': item.get('link'),
            'snippet': item.get('snippet')
        }
        if include_images and 'pagemap' in item and 'cse_image' in item['pagemap']:
            image_url = item['pagemap']['cse_image'][0]['src']
            image_path = save_image(image_url)
            entry['image'] = image_path
        data.append(entry)
    return data

def main():
    query = input("Enter your search query: ")
    num_results = int(input("Enter the number of results you want: "))
    include_images = input("Do you want to include images? (y/n): ").lower() == 'y'
    summarize = input("Do you want a summary of the results? (y/n): ").lower() == 'y'
    site_filter = input("Enter a website to filter results (e.g., linkedin.com) or press Enter to skip: ").strip()
    
    results = google_search(query, num_results, include_images, site_filter)
    data = parse_results(results, include_images)
    df = pd.DataFrame(data)
    print(df)
    
    if summarize:
        report = generate_report(df.to_dict(orient='records'))
        print("\nGenerated Report:\n")
        print(report)
    
    if include_images:
        input("Press Enter to delete downloaded images...")
        delete_images()

if __name__ == "__main__":
    main()
