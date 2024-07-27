import requests
import pandas as pd
import os
from image_handler import save_image, delete_images
from ai_integration import generate_report
from dotenv import load_dotenv
import tkinter as tk
from tkinter import ttk, messagebox

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

def run_terminal():
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

def run_gui():
    def on_search():
        query = entry_query.get()
        num_results = int(entry_num_results.get())
        include_images = var_include_images.get()
        summarize = var_summarize.get()
        site_filter = entry_site_filter.get().strip()
        
        results = google_search(query, num_results, include_images, site_filter)
        data = parse_results(results, include_images)
        df = pd.DataFrame(data)
        
        text_output.delete(1.0, tk.END)
        text_output.insert(tk.END, df.to_string(index=False) + '\n\n')
        
        if summarize:
            report = generate_report(df.to_dict(orient='records'))
            text_output.insert(tk.END, "Generated Report:\n")
            text_output.insert(tk.END, report)
        
        if include_images:
            # Show a message when images are downloaded (for demonstration purposes)
            messagebox.showinfo("Info", "Images have been downloaded and saved.")
    
    root = tk.Tk()
    root.title("Web Scraper GUI")

    # Create and place widgets
    tk.Label(root, text="Search Query:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
    entry_query = tk.Entry(root, width=50)
    entry_query.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(root, text="Number of Results:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
    entry_num_results = tk.Entry(root, width=50)
    entry_num_results.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(root, text="Include Images (y/n):").grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
    var_include_images = tk.BooleanVar()
    ttk.Checkbutton(root, variable=var_include_images).grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)

    tk.Label(root, text="Summarize Results (y/n):").grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
    var_summarize = tk.BooleanVar()
    ttk.Checkbutton(root, variable=var_summarize).grid(row=3, column=1, padx=10, pady=10, sticky=tk.W)

    tk.Label(root, text="Site Filter (e.g., linkedin.com):").grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)
    entry_site_filter = tk.Entry(root, width=50)
    entry_site_filter.grid(row=4, column=1, padx=10, pady=10)

    tk.Button(root, text="Search", command=on_search).grid(row=5, column=0, columnspan=2, pady=20)

    text_output = tk.Text(root, wrap=tk.WORD, height=20, width=80)
    text_output.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    root.mainloop()

def main():
    choice = input("Do you want to use GUI or Terminal? (Enter 'gui' or 'terminal'): ").strip().lower()
    if choice == 'gui':
        run_gui()
    elif choice == 'terminal':
        run_terminal()
    else:
        print("Invalid choice. Please enter 'gui' or 'terminal'.")

if __name__ == "__main__":
    main()
