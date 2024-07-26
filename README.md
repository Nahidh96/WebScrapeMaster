# WebScrapeMaster

# WebScrapeMaster

WebScrapeMaster is a Python-based web scraping tool that allows you to search the web using the Google Custom Search API, parse the results, and optionally include images and generate summaries.

## Features

- Search the web using Google Custom Search API
- Retrieve search results based on the search query
- Limit the number of search results to retrieve
- Filter results by specific websites
- Include images in the search results
- Generate summaries of the search results

## Prerequisites

Before getting started, make sure you have the following prerequisites:

- Python 3.6 or higher
- pip (Python package installer)
- Google Custom Search API key
- Google Custom Search Engine ID

## Setup

Follow these steps to set up the project:

1. Clone the Repository

    ```sh
    git clone https://github.com/yourusername/WebScrapeMaster.git
    cd WebScrapeMaster
    ```

2. Create a Virtual Environment

    It's recommended to use a virtual environment to manage dependencies.

    Activate the virtual environment:

    On Windows:

    ```sh
    venv\Scripts\activate
    ```

    On macOS/Linux:

    ```sh
    source venv/bin/activate
    ```

3. Install Dependencies

    Install the required Python packages using pip:

    ```sh
    pip install -r requirements.txt
    ```

4. Set Up Environment Variables

    Create a `.env` file in the root directory of the project and add your Google Custom Search API key and Search Engine ID:

    ```sh
    GOOGLE_API_KEY=your_api_key
    SEARCH_ENGINE_ID=your_search_engine_id
    ```

5. Run the Application

    You can now run the application:

    ```sh
    python main.py
    ```

## Usage

Follow these steps to use the application:

1. Enter your search query: When prompted, enter the search query you want to use.
2. Enter the number of results: Specify the number of search results you want to retrieve.
3. Include images: Choose whether to include images in the search results (y/n).
4. Generate summary: Choose whether to generate a summary of the search results (y/n).

