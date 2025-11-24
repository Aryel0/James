import requests
import os
from datetime import datetime

os.makedirs("results", exist_ok=True)

# Headers to avoid 403 errors
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# DuckDuckGo HTML search (more reliable than their API)
def duckduckgo_search(query: str):
    """Search DuckDuckGo for current information"""
    try:
        # Use DuckDuckGo Instant Answer API with better parsing
        url = "https://api.duckduckgo.com/"
        params = {
            "q": query, 
            "format": "json", 
            "no_html": 1, 
            "skip_disambig": 1
        }
        res = requests.get(url, params=params, headers=HEADERS, timeout=10)
        data = res.json()
        
        results = []
        
        # Try AbstractText first
        if data.get("AbstractText"):
            results.append(data["AbstractText"])
        
        # Then try Related Topics
        if data.get("RelatedTopics"):
            for topic in data["RelatedTopics"][:3]:
                if isinstance(topic, dict) and topic.get("Text"):
                    results.append(topic["Text"])
        
        # Try Answer field
        if data.get("Answer"):
            results.append(data["Answer"])
        
        if results:
            return "\n\n".join(results)
        
        # Fallback: try Wikipedia directly for this query
        return f"DuckDuckGo returned no results. Suggestion: Try using the 'wikipedia' tool for '{query}'"
        
    except Exception as e:
        return f"Search error: {str(e)}. Try using the 'wikipedia' tool instead."

# Wikipedia search with proper headers
def wikipedia_search(query: str):
    """Search Wikipedia for detailed information"""
    try:
        # Clean up query for URL
        query_formatted = query.replace(" ", "_")
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query_formatted}"
        
        # Add User-Agent to avoid 403
        res = requests.get(url, headers=HEADERS, timeout=10)
        
        if res.status_code == 200:
            data = res.json()
            extract = data.get("extract", "")
            if extract:
                title = data.get("title", query)
                page_url = data.get("content_urls", {}).get("desktop", {}).get("page", "")
                return f"**{title}**\n\n{extract}\n\nSource: {page_url}"
            return "No summary available for this topic."
        elif res.status_code == 404:
            return f"No Wikipedia page found for '{query}'. Try a different search term or use the 'search' tool."
        else:
            return f"Wikipedia error {res.status_code}. Try rephrasing your query or use the 'search' tool."
    except Exception as e:
        return f"Wikipedia error: {str(e)}"

# Save tool with confirmation
def save_to_file(text: str):
    """Save text to a file in the results directory"""
    try:
        if not text or len(text.strip()) == 0:
            return "Error: Cannot save empty text."
        
        filename = f"results/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(text)
        
        file_size = os.path.getsize(filename)
        return f"Successfully saved {file_size} bytes to {filename}"
    except Exception as e:
        return f"Error saving file: {str(e)}"

# Tool dictionary for easy access
TOOLS = {
    "search": duckduckgo_search,
    "wikipedia": wikipedia_search,
    "save": save_to_file,
}

# Tool metadata for documentation
TOOL_DESCRIPTIONS = {
    "search": "Use DuckDuckGo to search for current information. Args: query (str)",
    "wikipedia": "Search Wikipedia for detailed information. Args: query (str)",
    "save": "Save text to a file in the results directory. Args: text (str)",
}

def get_tool_descriptions():
    """Return a formatted string of all available tools and their descriptions"""
    return "\n".join([f"- {name}: {desc}" for name, desc in TOOL_DESCRIPTIONS.items()])