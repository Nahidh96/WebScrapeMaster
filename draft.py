import os
import json
from crawl4ai import WebCrawler
import cohere
import urllib.parse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create an instance of WebCrawler
crawler = WebCrawler()

# Warm up the crawler (load necessary models)
crawler.warmup()

# Function to get the URL based on user input
def get_url():
    choice = input("Enter '1' for Google search or '2' for a specific website: ")
    if choice == '1':
        search_query = input("Enter your search query: ")
        # Encode the search query for use in the URL
        encoded_query = urllib.parse.quote_plus(search_query)
        url = f"https://www.google.com/search?q={encoded_query}&rlz=1C1CHBD_en-GBLK1096LK1096&oq={encoded_query}&gs_lcrp=EgZjaHJvbWUqCAgBEEUYJxg7MgYIABBFGDkyCAgBEEUYJxg7MgYIAhAjGCcyCggDEAAYgAQYogQyCggEEAAYgAQYogQyBggFEEUYPDIGCAYQRRg8MgYIBxBFGDzSAQgyNzk5ajBqN6gCALACAA&sourceid=chrome&ie=UTF-8"
    elif choice == '2':
        website = input("Enter the website URL: ")
        url = website
    else:
        print("Invalid choice. Exiting...")
        exit()
    return url

# Run the crawler on a URL
url = get_url()
result = crawler.run(url=url)

# Extract the content in markdown format
content = result.markdown

# Initialize Cohere client
cohere_client = cohere.Client(os.getenv("COHERE_API_KEY"))

# Define the prompt for summarization
instructions = (
    "From the content, extract the following details, ensuring that the sentences make sense and are in complete English: "
    "1. Title of the page "
    "2. Summary of the page in detail "
    "3. Brief summary of the page in a paragraph "
    "4. Keywords assigned to the page as a list of keywords. "
    "The extracted JSON format should look like this: "
    '{ "title": "Page Title", "summary": "Detailed summary of the page.", "brief_summary": "Brief summary in a paragraph.", "keywords": ["keyword1", "keyword2", "keyword3"] }'
)

# Combine instructions with content
full_prompt = instructions + "\n\nContent:\n" + content

# Generate the summary using Cohere
try:
    response = cohere_client.generate(
        model='command-xlarge-nightly',
        prompt=full_prompt,
        max_tokens=3000  # Adjust as needed
    )
    
    # Print raw response for debugging
    raw_response = response.generations[0].text
    print("Raw Cohere Response:")
    print(raw_response)

    # Parse the extracted summary into JSON
    try:
        summary_json = json.loads(raw_response)
    except json.JSONDecodeError:
        summary_json = {"error": "Failed to decode JSON from Cohere response"}
    
    # Extract the detailed summary part
    detailed_summary = summary_json.get("summary", "No detailed summary found.")
    print("\nDetailed Summary:")
    print(detailed_summary)

except Exception as e:
    summary_json = {"error": str(e)}

# Save the JSON to a file
with open("page_summary.json", "w") as file:
    json.dump(summary_json, file, indent=4)

print("Summary saved to page_summary.json")
