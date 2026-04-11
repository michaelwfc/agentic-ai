
from langchain_core.tools import tool
from langchain_community.document_loaders import WikipediaLoader

@tool
def search_wikipedia(query: str):
    
    """ Retrieve docs from wikipedia """

    # Search
    search_docs = WikipediaLoader(query=query,  load_max_docs=2).load()

     # Format
    formatted_search_docs = "\n\n---\n\n".join(
        [
            f'<Document source="{doc.metadata["source"]}" page="{doc.metadata.get("page", "")}">\n{doc.page_content}\n</Document>'
            for doc in search_docs
        ]
    )

    return {"context": [formatted_search_docs]} 