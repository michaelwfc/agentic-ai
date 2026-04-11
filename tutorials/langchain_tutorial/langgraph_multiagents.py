from typing import Any, List, Annotated
from typing_extensions import TypedDict
import operator
from operator import add

from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from utils.langchain_utils import save_graph_image
from utils.qwen_api import init_langchain_chat_openai


def node_1(state):
    print("---Node 1---")
    return {"foo": [state['foo'][-1] + 1]}

def node_2(state):
    print("---Node 2---")
    return {"foo": [state['foo'][-1] + 1]}

def node_3(state):
    print("---Node 3---")
    return {"foo": [state['foo'][-1] + 1]}
  


def reduce_list(left: list | None, right: list | None) -> list:
    """Safely combine two lists, handling cases where either or both inputs might be None.

    Args:
        left (list | None): The first list to combine, or None.
        right (list | None): The second list to combine, or None.

    Returns:
        list: A new list containing all elements from both input lists.
               If an input is None, it's treated as an empty list.
    """
    if not left:
        left = []
    if not right:
        right = []
    return left + right

class DefaultState(TypedDict):
    foo: Annotated[list[int], add]

class CustomReducerState(TypedDict):
    foo: Annotated[list[int], reduce_list]
    


class SimpleNodeAgent:

    def build_graph(self) -> CompiledStateGraph:
      # Build graph
      builder = StateGraph(CustomReducerState)
      builder.add_node("node_1", node_1)
      builder.add_node("node_2", node_2)
      builder.add_node("node_3", node_3)

      # Logic
      builder.add_edge(START, "node_1")
      builder.add_edge("node_1", "node_2")
      builder.add_edge("node_1", "node_3")
      builder.add_edge("node_2", END)
      builder.add_edge("node_3", END)

      # Add
      graph = builder.compile()
      return graph
      
    def run(self) -> List[str]:
      graph = self.build_graph()
      output = graph.invoke({"foo": [1]})
      print(output)
      return output

      


  
  

class State(TypedDict):
    # Note, no reducer function. 
    state: Annotated[List[str], operator.add]
    
    
def sorting_reducer(left, right):
    """ Combines and sorts the values in a list"""
    if not isinstance(left, list):
        left = [left]

    if not isinstance(right, list):
        right = [right]
    
    return sorted(left + right, reverse=False)
  
class OrderedState(TypedDict):
    state: Annotated[List[str], sorting_reducer]
    
    
class ReturnNodeValue:
    def __init__(self, node_secret: str):
        self._value = node_secret

    def __call__(self, state: State|OrderedState) -> Any:
        print(f"Adding {self._value} to {state['state']}")
        return {"state": [self._value]}
      
      
    
class SimpleMuiltiAgent:

    def __init__(self):
      pass
    
    def build_sequence_graph(self) -> CompiledStateGraph:
      # Add nodes
      builder = StateGraph(State)

      # Initialize each node with node_secret 
      builder.add_node("a", ReturnNodeValue("I'm A"))
      builder.add_node("b", ReturnNodeValue("I'm B"))
      builder.add_node("c", ReturnNodeValue("I'm C"))
      builder.add_node("d", ReturnNodeValue("I'm D"))

      # Flow
      builder.add_edge(START, "a")
      builder.add_edge("a", "b")
      builder.add_edge("b", "c")
      builder.add_edge("c", "d")
      builder.add_edge("d", END)
      graph = builder.compile()
      save_graph_image(graph, "simple_multi_agent.png")
      return graph
  
  
    def build_parallel_graph(self) -> CompiledStateGraph:
      builder = StateGraph(State)
      builder.add_node("a", ReturnNodeValue("I'm A"))
      builder.add_node("b", ReturnNodeValue("I'm B"))
      builder.add_node("c", ReturnNodeValue("I'm C"))
      builder.add_node("d", ReturnNodeValue("I'm D"))
      
      builder.add_edge(START, "a")
      builder.add_edge("a", "b")
      builder.add_edge("a", "c")
      builder.add_edge("b", "d")
      builder.add_edge("c", "d")
      builder.add_edge("d", END)
      graph = builder.compile()
      save_graph_image(graph, "simple_parallel_agent.png")
      return graph
    
    def build_parallel_graph_v2(self) -> CompiledStateGraph:
      # builder = StateGraph(State)
      builder = StateGraph(OrderedState)
      
      # Initialize each node with node_secret 
      builder.add_node("a", ReturnNodeValue("I'm A"))
      builder.add_node("b", ReturnNodeValue("I'm B"))
      builder.add_node("b2", ReturnNodeValue("I'm B2"))
      builder.add_node("c", ReturnNodeValue("I'm C"))
      builder.add_node("d", ReturnNodeValue("I'm D"))

      # Flow
      builder.add_edge(START, "a")
      builder.add_edge("a", "b")
      builder.add_edge("a", "c")
      builder.add_edge("b", "b2")
      builder.add_edge(["b2", "c"], "d")
      builder.add_edge("d", END)
      graph = builder.compile()
      save_graph_image(graph, "simple_parallel_agent_v2.png")
      return graph
    
      
    
    def run(self,) -> List[str]:
      # graph = self.build_sequence_graph()
      # graph = self.build_parallel_graph()
      graph = self.build_parallel_graph_v2()
      
      output = graph.invoke({"state": []})
      print(output)
      
if __name__ == "__main__":
      # agent = SimpleNodeAgent()
      # agent.run()
      
  
      agent = SimpleMuiltiAgent()
      agent.run()
      

      