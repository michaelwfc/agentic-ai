"""
### Access and modify state within tools
#### State
One of the nice features of LangGraph is state. The graph has a typed data structure that is available to each node for the duration of the graph and can be persisted in long-term storage. You can use this to store information to share between nodes, to debug the graph, and to reset a long-running graph to an earlier time.

When you define state for a graph, you define the data types and a 'reducer' function. The reducer describes how information is added to that element. This is especially useful when a task is mapped to multiple nodes, which are executed in parallel and update state simultaneously.

In this example, the default `AgentState` was used. This is defined in [langgraph.prebuilt.chat_agent_executor](https://github.com/langchain-ai/langgraph/blob/e365b2b8bd695e03d758b19ff109152b2e342a87/libs/prebuilt/langgraph/prebuilt/chat_agent_executor.py).   

```python
    class AgentState(TypedDict):
        "The state of the agent."
        messages: Annotated[Sequence[BaseMessage], add_messages]
        remaining_steps: NotRequired[RemainingSteps]
```
        
- `messages` are a list of `BaseMessage`, defined in [langchain_core](https://github.com/langchain-ai/langchain/blob/088095b663993b1e53cf616e1ca487d1739b0d71/libs/core/langchain_core/messages/base.py), which contains the messages to and from the LLM.
    - typing.Annotated allows you to attach arbitrary metadata to a type hint. Syntax: Annotated[Type, metadata1, metadata2, ...] 
- The `add_messages` reducer will append new messages to the end of the message list.  
- `remaining_steps` tracks the steps in a graph. You will see this initialized as the `recursion_limit`, but is tracked by the graph and not visibile to the user.  
Let's take a look at this quickly.
"""


from typing import Annotated, List, Literal, Union, NotRequired
from typing_extensions import TypedDict
from langchain.agents import AgentState



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


class CalcState(AgentState):
    """Graph State."""
    ops: Annotated[List[str], reduce_list]



"""State management for deep agents with TODO tracking and virtual file systems.

This module defines the extended agent state structure that supports:
- Task planning and progress tracking through TODO lists
- Context offloading through a virtual file system stored in state
- Efficient state merging with reducer functions
"""

class Todo(TypedDict):
    """A structured task item for tracking progress through complex workflows.

    Attributes:
        content: Short, specific description of the task
        status: Current state - pending, in_progress, or completed
    """

    content: str
    status: Literal["pending", "in_progress", "completed"]


def file_reducer(left, right):
    """Merge two file dictionaries, with right side taking precedence.

    Used as a reducer function for the files field in agent state,
    allowing incremental updates to the virtual file system.

    Args:
        left: Left side dictionary (existing files)
        right: Right side dictionary (new/updated files)

    Returns:
        Merged dictionary with right values overriding left values
    """
    if left is None:
        return right
    elif right is None:
        return left
    else:
        return {**left, **right}


class DeepAgentState(AgentState):
    """Extended agent state that includes task tracking and virtual file system.

    Inherits from LangGraph's AgentState and adds:
    - todos: List of Todo items for task planning and progress tracking
    - files: Virtual file system stored as dict mapping filenames to content
    """

    todos: NotRequired[list[Todo]]
    files: Annotated[NotRequired[dict[str, str]], file_reducer]