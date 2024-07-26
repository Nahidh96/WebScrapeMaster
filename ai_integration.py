import cohere

# Replace with your Cohere API key
COHERE_API_KEY = 'AXCXgZktGSHLT4mPpJh0v4upucX2imVKWdaowDIZ'

def generate_report(data):
    text_data = ""
    for item in data:
        text_data += f"Title: {item['title']}\nLink: {item['link']}\nSnippet: {item['snippet']}\n\n"
    
    prompt = f"You are an expert in organizing information. Please create a detailed and well-structured report based on the following search results. Present the information in a coherent and readable format. Each result includes a title, link, and snippet. Here are the results:\n{text_data}"
    
    co = cohere.Client(COHERE_API_KEY)
    
    response = co.summarize(
        text=prompt,
        model='summarize-xlarge',  # Use an appropriate model, adjust as needed
        length='medium',  # Adjust the length of the summary
        format='paragraph',  # Adjust the format of the summary
    )
    
    summary = response.summary
    return summary
