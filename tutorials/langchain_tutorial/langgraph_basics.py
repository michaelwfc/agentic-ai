from pprint import pprint
import random
from typing import Dict, Literal, List, Annotated
from urllib import response
from google_crc32c import value
from typing_extensions import TypedDict
from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import ToolNode,tools_condition

from langchain_core.messages import (
    SystemMessage,
    AIMessage,
    HumanMessage,
    ToolMessage,
    AnyMessage,
)
from langgraph.graph.message import add_messages, MessagesState
from utils.env_utils import load_env
from utils.qwen_api import init_langchain_chat_openai
from utils.langchain_utils import save_graph_image, save_graph_as_markdown


"""
State
- https://docs.langchain.com/oss/python/langgraph/graph-api#state
The State schema serves as the input schema for all Nodes and Edges in the graph.

Let's use the TypedDict class from python's typing module as our schema, which provides type hints for the keys.
"""


class State(TypedDict):
    graph_state: str


# class MessageState(TypedDict):
#     messages: Annotated[List[AnyMessage], add_messages]

MAX_TOOL_LOOPS = 5  # Set your max here (e.g., 5 iterations)


class ExtendedMessagesState(MessagesState):
    # Add any keys needed beyond messages, which is pre-built
    tool_loop_count: int = 0  # New: Specific counter for tool_calling_llm loops


def run_add_messages():
    """https://docs.langchain.com/oss/python/langgraph/graph-api#message-state"""
    # Initial state
    initial_messages = [
        AIMessage(content="Hello! How can I assist you?", name="Model"),
        HumanMessage(
            content="I'm looking for information on marine biology.", name="Lance"
        ),
    ]

    # New message to add
    new_message = AIMessage(
        content="Sure, I can help with that. What specifically are you interested in?",
        name="Model",
    )

    # Test
    messages = add_messages(initial_messages, new_message)
    for m in messages:
        m.pretty_print()


"""
Nodes
- https://docs.langchain.com/oss/python/langgraph/graph-api#nodes
- https://docs.langchain.com/oss/python/langgraph/graph-api#reducers
Nodes are just python functions.

The first positional argument is the state, as defined above.

Because the state is a TypedDict with schema as defined above, each node can access the key, graph_state, with state['graph_state'].

Each node returns a new value of the state key graph_state.

By default, the new value returned by each node will override the prior state value.

"""


def node_1(state):
    print("---Node 1---")
    return {"graph_state": state["graph_state"] + " I am"}


def node_2(state):
    print("---Node 2---")
    return {"graph_state": state["graph_state"] + " happy!"}


def node_3(state):
    print("---Node 3---")
    return {"graph_state": state["graph_state"] + " sad!"}


"""
Edges
- https://docs.langchain.com/oss/python/langgraph/graph-api#edges
- https://docs.langchain.com/oss/python/langgraph/graph-api#conditional-edges

Edges connect the nodes.

Normal Edges are used if you want to always go from, for example, node_1 to node_2.

Conditional Edges are used if you want to optionally route between nodes.

Conditional edges are implemented as functions that return the next node to visit based on some logic.
"""


def decide_mood(state) -> Literal["node_2", "node_3"]:

    # Often, we will use state to decide on the next node to visit
    user_input = state["graph_state"]

    # Here, let's just do a 50 / 50 split between nodes 2, 3
    if random.random() < 0.5:

        # 50% of the time, we return Node 2
        return "node_2"

    # 50% of the time, we return Node 3
    return "node_3"


"""
Graph Construction
- https://docs.langchain.com/oss/python/langgraph/graph-api#stategraph

Now, we build the graph from our components defined above.

The StateGraph class is the graph class that we can use.

First, we initialize a StateGraph with the State class we defined above.

Then, we add our nodes and edges.

We use the START Node, a special node that sends user input to the graph, to indicate where to start our graph.

The END Node is a special node that represents a terminal node.

Finally, we compile our graph to perform a few basic checks on the graph structure.

We can visualize the graph as a Mermaid diagram.
"""


def run_simple_graph():
    # Build graph
    builder = StateGraph(State)
    builder.add_node("node_1", node_1)
    builder.add_node("node_2", node_2)
    builder.add_node("node_3", node_3)

    # Logic
    builder.add_edge(START, "node_1")
    builder.add_conditional_edges("node_1", decide_mood)
    builder.add_edge("node_2", END)
    builder.add_edge("node_3", END)

    # Add
    graph = builder.compile()
    print("Graph built successfully!")

    # Run
    inputs = {"graph_state": "Hi, this is Lance."}
    result = graph.invoke(inputs)
    print(result)

    return graph


def multiply(a: int, b: int) -> int:
    """Multiply a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b

# This will be a tool
def add(a: int, b: int) -> int:
    """Adds a and b.

    Args:
        a: first int
        b: second int
    """
    return a + b

def divide(a: int, b: int) -> float:
    """Divide a and b.

    Args:
        a: first int
        b: second int
    """
    return a / b
  

def run_chat_model():
    messages = [
        AIMessage(
            content=f"So you said you were researching ocean mammals?", name="Model"
        )
    ]
    messages.append(HumanMessage(content=f"Yes, that's right.", name="Lance"))
    messages.append(
        AIMessage(content=f"Great, what would you like to learn about.", name="Model")
    )
    messages.append(
        HumanMessage(
            content=f"I want to learn about the best place to see Orcas in the US.",
            name="Lance",
        )
    )

    llm = init_langchain_chat_openai()

    # for m in messages:
    #     m.pretty_print()

    # result = llm.invoke(messages)
    # print(type(result))
    # print(result.response_metadata)

    llm_with_tools = llm.bind_tools([multiply])

    tool_call = llm_with_tools.invoke(
        [HumanMessage(content=f"What is 2 multiplied by 3", name="Lance")]
    )
    print(tool_call.tool_calls)


def run_chat_model_stream():
    llm = init_langchain_chat_openai()
    llm_with_tools = llm.bind_tools([multiply])

    question_01 = "What is 2 multiplied by 3"
    question_02 = "Hello, how are you?"
    question_03 = "What is two multiplied by 3"

    question = question_01  # Change as needed

    stream = llm_with_tools.stream([HumanMessage(content=question, name="Lance")])

    for i, chunk in enumerate(stream):
        print(f"Chunk {i}:")
        print(f"  Content: {chunk.content}")

        if chunk.tool_calls:  # Check if there are tool calls in this chunk
            for tool_call in chunk.tool_calls:
                tool_name = tool_call.get("name")  # e.g., 'multiply'
                tool_args = tool_call.get("args", {})  # e.g., {'a': 2, 'b': 3}
                tool_id = tool_call.get("id")  # e.g., 'call_123'

                print(f"  Tool Name: {tool_name}")
                print(f"  Tool Args: {tool_args}")
                print(f"  Tool ID: {tool_id}")

                # Optional: You can accumulate or process the tool calls here
                # For example, store them in a list for later execution
        else:
            print("  No tool calls in this chunk.")


"""
ToolNode: This is a prebuilt LangGraph utility that simplifies tool execution. It takes your tools (e.g., [multiply]) and automatically:
- Extracts tool calls from the last message.
- Executes them.
- Appends ToolMessage objects (with results) to the message history.

If you prefer manual implementation (without ToolNode), you could write a custom node like this:



"""


def execute_tools(state: MessagesState) -> Dict[str, AnyMessage]:
    messages = state["messages"]
    last_message = messages[-1]
    tool_results = []
    if hasattr(last_message, "tool_calls"):
        for tool_call in last_message.tool_calls:
            try:
                if tool_call["name"] == "multiply":
                    result = multiply(**tool_call["args"])  # Execute the tool
                    tool_results.append(
                        ToolMessage(
                            content=str(result),  # Convert result to string
                            tool_call_id=tool_call["id"],
                        )
                    )
                else:
                    # Handle unknown tools (optional, for future expansion)
                    tool_results.append(
                        ToolMessage(
                            content=f"Error: Unknown tool: {tool_call['name']}",
                            tool_call_id=tool_call["id"],
                        )
                    )
            except Exception as e:
                # Handle any failure (e.g., invalid args, KeyError, TypeError)
                tool_results.append(
                    ToolMessage(
                        content=f"Error executing tool: {e}",
                        tool_call_id=tool_call["id"],
                    )
                )
    return {"messages": tool_results}


# Conditional Edge (should_continue): This function inspects the last message. If it contains tool calls, it routes to the "tools" node. Otherwise, it ends the graph. This prevents infinite loops and ensures the graph only executes tools when needed.


# Loop Back Edge: After tool execution, the graph routes back to tool_calling_llm. This allows the LLM to process the tool results and generate a final response (e.g., "The result is 6").
# add conditional edge to check for tool calls in the last message
def should_continue(state: ExtendedMessagesState) -> Literal["execute_tools", END]:
    messages = state["messages"]
    last_message = messages[-1]

    tool_loop_count = state.get("tool_loop_count", 0)

    if tool_loop_count >= MAX_TOOL_LOOPS:
        print(
            f"Reached max tool loops ({MAX_TOOL_LOOPS}). Ending graph to prevent infinite loop."
        )
        return END

    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "execute_tools"  # Route to tool execution node
    else:
        return END




# define node for llm with tools
def tool_calling_llm(state: ExtendedMessagesState) -> Dict[str, AnyMessage]:
    messages = state["messages"]
    result = llm_with_tools.invoke(messages)
    # Increment only the tool-specific counter
    return {
        "messages": result,
        "tool_loop_count": state.get("tool_loop_count", 0) + 1,
    }  # Pass loop_count through state

def build_graph_with_tool_calling_v1(save_graph: bool = False) -> CompiledStateGraph:

    builder = StateGraph(ExtendedMessagesState)
    builder.add_node("tool_calling_llm", tool_calling_llm)
    builder.add_edge(START, "tool_calling_llm")

    # add tool execution node
    builder.add_node("execute_tools", execute_tools)
    builder.add_conditional_edges("tool_calling_llm", should_continue)

    # # Route back to LLM for tool execution ?
    # Missing Edge: After execute_tools runs, the graph needs to route back to "tool_calling_llm" so the LLM can process the tool results and generate a final response (e.g., "The result is 6"). Without this, the graph will end after tool execution, leaving you with raw tool messages instead of a complete response.
    builder.add_edge("execute_tools", "tool_calling_llm")

    # builder.add_edge("tool_calling_llm", END)
    graph = builder.compile()

    if save_graph:
        save_graph_image(graph, filename="graph_with_tool_calling_v1.png")
    return graph


def build_graph_with_tool_calling_v2(save_graph: bool = False) -> CompiledStateGraph:
  """This version simplifies the graph by using a ToolNode, which automatically handles tool calls and execution. The conditional edge now only checks for the presence of tool calls to determine whether to route to the ToolNode or end the graph."""

  builder = StateGraph(ExtendedMessagesState)
  builder.add_node("tool_calling_llm", tool_calling_llm)
  builder.add_edge(START, "tool_calling_llm")
  
  # add ToolNode for automatic tool execution
  builder.add_node("tools", ToolNode([multiply]))
  # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
  # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
  builder.add_conditional_edges("tool_calling_llm", tools_condition)
  
  builder.add_edge("tools", "tool_calling_llm")  # Loop back to LLM after tool execution
  graph = builder.compile()
  if save_graph:
    save_graph_image(graph, filename="graph_with_tool_calling_v2.png")
  return graph
  




def run_graph_with_tool_calling(version: int = 1, save_graph: bool = False):

    question = QUESTION_03
    if version == 1:
        graph = build_graph_with_tool_calling_v1()
    elif version == 2:
        graph = build_graph_with_tool_calling_v2(save_graph=save_graph)
        

    messages = graph.invoke(
        {
            "messages": [HumanMessage(content=question, name="Lance")],
            "tool_loop_count": 0,
        }  # Initialize here to ensure it's in the state
    )
    for m in messages["messages"]:
        m.pretty_print()


def run_graph_with_tool_calling_stream():
    question = QUESTION_02
    graph = build_graph_with_tool_calling_v1()
    stream = graph.stream(
        {
            "messages": [HumanMessage(content=question, name="Lance")],
            "tool_loop_count": 0,
        }
    )

    accumulated_state = {}
    for i, chunk in enumerate(stream):
        print(f"\n=== Chunk {i} ===")
        # Merge chunk updates into accumulated state
        for node_name, state_update in chunk.items():
            for key, value in state_update.items():
                if isinstance(value, list):
                    accumulated_state.setdefault(key, []).extend(value)
                else:
                    accumulated_state.setdefault(key, []).extend([value])

        # Now you can access full state
        if "messages" in accumulated_state:
            last_msg = accumulated_state["messages"][-1]
            last_msg.pretty_print()




def build_math_agent_graph(save_graph: bool = False) -> CompiledStateGraph:
    llm = init_langchain_chat_openai()
    tools = [multiply, add, divide]
    llm_with_tools = llm.bind_tools(tools, parallel_tool_calls=False)
    
    # System message
    sys_msg = SystemMessage(content="You are a helpful assistant tasked with performing arithmetic on a set of inputs.")
    # Node
    def assistant(state: MessagesState):
      return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}
    
    
    
    builder = StateGraph(ExtendedMessagesState)
    # rename tool_calling_llm to agent for clarity in this context
    builder.add_node("agent", assistant)
    builder.add_edge(START, "agent")

    # add ToolNode for automatic tool execution
    builder.add_node("tools", ToolNode(tools))
    builder.add_conditional_edges("agent", tools_condition)
    
    builder.add_edge("tools", "agent")  # Loop back to LLM after tool execution
    graph = builder.compile()
    if save_graph:
        save_graph_image(graph, filename="math_agent_graph.png")
    return graph
  

def run_math_agent_graph(save_graph: bool = False):
    question = QUESTION_04
    graph = build_math_agent_graph(save_graph=save_graph)
    messages = [HumanMessage(content=question, name="Lance")]
    messages = graph.invoke(
        {
            "messages": messages,
            "tool_loop_count": 0,
        }  # Initialize here to ensure it's in the state``
    )
  
    for m in messages["messages"]:
        m.pretty_print()  
    
  
  
if __name__ == "__main__":
    load_env()

    QUESTION_01 = "What is 2 multiplied by 3"
    QUESTION_02 = f"Hello, how are you?"
    QUESTION_03 = "What is too multiplied by 3"
    QUESTION_04 = "What is 2 multiplied by 3, then add 4, then divide by 2?"

    # llm = init_langchain_chat_openai()
    # llm_with_tools = llm.bind_tools([multiply])
    # print("Graph built successfully!")
    # run_simple_graph()

    # run_chat_model()
    # run_chat_model_stream()

    # run_add_messages()

    # run_graph_with_tool_calling(version=2, save_graph=True)

    # run_graph_with_tool_calling_stream()
    
    run_math_agent_graph(save_graph=True)
    
    
    
