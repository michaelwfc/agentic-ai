"""
Tavily for web search

Tavily Search API is a search engine optimized for LLMs, aimed at efficient, quick, and persistent search results. You can sign up for an API key here(https://app.tavily.com/home).
It’s easy to sign up and offers a generous free tier. We'll use Tavily for building research agents with external search.



"""

from langchain_core.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from utils.env_utils import load_env


def run_tavily_search():

    # Initialize the Tavily Search Tool
    tavily_search = TavilySearchResults(max_results=3)

    # Example search query
    query = "What is the Model Context Protocol (MCP) developed by Anthropic?"

    # Call the search tool with the query
    search_results = tavily_search.invoke(query)

    # Print the search results

    return search_results


# Mock search result
search_result = """The Model Context Protocol (MCP) is an open standard protocol developed 
by Anthropic to enable seamless integration between AI models and external systems like 
tools, databases, and other services. It acts as a standardized communication layer, 
allowing AI models to access and utilize data from various sources in a consistent and 
efficient manner. Essentially, MCP simplifies the process of connecting AI assistants 
to external services by providing a unified language for data exchange. """



@tool
def web_search(
    query: str,
) -> str:
    """Search the web for information on a specific topic.

    This tool performs web searches and returns relevant results
    for the given query. Use this when you need to gather information from
    the internet about any topic.

    Args:
        query: The search query string. Be specific and clear about what
               information you're looking for.

    Returns:
        Search results from search engine.

    Example:
        web_search("machine learning applications in healthcare")
    """
    # Initialize the Tavily Search Tool
    tavily_search = TavilySearchResults(max_results=3)

    # Call the search tool with the query
    data = tavily_search.invoke({"query": query})
    search_docs = data.get("results", data)

    # Format
    formatted_search_docs = "\n\n---\n\n".join(
        [
            f'<Document href="{doc["url"]}">\n{doc["content"]}\n</Document>'
            for doc in search_docs
        ]
    )
    return formatted_search_docs


if __name__ == "__main__":
    load_env()

    search_results = run_tavily_search()
    for r in search_results:
        print(r.keys())
