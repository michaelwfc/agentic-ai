
from typing import List, Dict, Text, Annotated,TypedDict
import operator

from langchain_core.messages import (
    SystemMessage,
    AIMessage,
    HumanMessage,
    AnyMessage,
    ToolMessage,
)
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain_community.document_loaders import WikipediaLoader
from langchain_tavily import TavilySearch  # updated since filming


from utils.env_utils import load_env
from utils.qwen_api import init_langchain_chat_openai
from utils.langchain_utils import save_graph_image



  
class SearchState(TypedDict):
    question: str
    answer: str
    context: Annotated[list, operator.add]
    
    

def search_web(state:SearchState):
    
    """ Retrieve docs from web search """
    # Search
    tavily_search = TavilySearch(max_results=3)
    question = state['question']
    data = tavily_search.invoke({"query": question})
    search_docs = data.get("results", data)

     # Format
    formatted_search_docs = "\n\n---\n\n".join(
        [
            f'<Document href="{doc["url"]}">\n{doc["content"]}\n</Document>'
            for doc in search_docs
        ]
    )

    return {"context": [formatted_search_docs]} 

def search_wikipedia(state:SearchState):
    
    """ Retrieve docs from wikipedia """

    # Search
    search_docs = WikipediaLoader(query=state['question'], 
                                  load_max_docs=2).load()

     # Format
    formatted_search_docs = "\n\n---\n\n".join(
        [
            f'<Document source="{doc.metadata["source"]}" page="{doc.metadata.get("page", "")}">\n{doc.page_content}\n</Document>'
            for doc in search_docs
        ]
    )

    return {"context": [formatted_search_docs]} 
  

    
    
class SimpleResearchAgent():
    def __init__(self):
       
        self.tools = []
        self.llm = init_langchain_chat_openai()
        self.memory = MemorySaver()
        
        
    def generate_answer(self, state):
    
        """ Node to answer a question """

        # Get state
        context = state["context"]
        question = state["question"]

        # Template
        answer_template = """Answer the question {question} using this context: {context}"""
        answer_instructions = answer_template.format(question=question, 
                                                          context=context)    
        
        # Answer
        answer = self.llm.invoke([SystemMessage(content=answer_instructions)]+[HumanMessage(content=f"Answer the question.")])
          
        # Append it to state
        return {"answer": answer}
            
    def build_graph(self) -> CompiledStateGraph:
        builder = StateGraph(SearchState)
        
        # Initialize each node with node_secret 
        builder.add_node("search_web",search_web)
        builder.add_node("search_wikipedia", search_wikipedia)
        builder.add_node("generate_answer", self.generate_answer)

        # Flow
        builder.add_edge(START, "search_wikipedia")
        builder.add_edge(START, "search_web")
        builder.add_edge("search_wikipedia", "generate_answer")
        builder.add_edge("search_web", "generate_answer")
        builder.add_edge("generate_answer", END)
        graph = builder.compile()

        save_graph_image(graph, "simple_research_agent.png")
        return graph
      
    def run(self, question: str="How were Nvidia's Q2 2025 earnings") -> str:
        """ Run the agent """
        graph = self.build_graph()
        # Run
        state = graph.invoke({"question": question})
        
        # Return
        return state["answer"]
  


if __name__ == "__main__":
  
      load_env()
      agent = SimpleResearchAgent()
      print(agent.run())  
