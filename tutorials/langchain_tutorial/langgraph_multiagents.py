from typing import Any, List, Annotated, Optional
from typing_extensions import TypedDict
import operator
from operator import add

from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from langgraph.checkpoint.memory import MemorySaver

from utils.langchain_utils import save_graph_image
from utils.qwen_api import init_langchain_chat_openai


def node_1(state):
    print("---Node 1---")
    return {"foo": [state["foo"][-1] + 1]}


def node_2(state):
    print("---Node 2---")
    return {"foo": [state["foo"][-1] + 1]}


def node_3(state):
    print("---Node 3---")
    return {"foo": [state["foo"][-1] + 1]}


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
    """Combines and sorts the values in a list"""
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

    def __call__(self, state: State | OrderedState) -> Any:
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

    def run(
        self,
    ) -> List[str]:
        # graph = self.build_sequence_graph()
        # graph = self.build_parallel_graph()
        graph = self.build_parallel_graph_v2()

        output = graph.invoke({"state": []})
        print(output)


# The structure of the logs
class Log(TypedDict):
    id: str
    question: str
    docs: Optional[List]
    answer: str
    grade: Optional[int]
    grader: Optional[str]
    feedback: Optional[str]


# Failure Analysis Sub-graph
class FailureAnalysisState(TypedDict):
    cleaned_logs: List[Log]
    failures: List[Log]
    fa_summary: str
    processed_logs: List[str]


class FailureAnalysisOutputState(TypedDict):
    fa_summary: str
    processed_logs: List[str]


def get_failures(state):
    """Get logs that contain a failure"""
    cleaned_logs = state["cleaned_logs"]
    failures = [log for log in cleaned_logs if "grade" in log]
    return {"failures": failures}


def generate_failures_summary(state):
    """Generate summary of failures"""
    failures = state["failures"]
    # Add fxn: fa_summary = summarize(failures)
    fa_summary = "Poor quality retrieval of Chroma documentation."
    return {
        "fa_summary": fa_summary,
        "processed_logs": [
            f"failure-analysis-on-log-{failure['id']}" for failure in failures
        ],
    }


class FailureAnalysisAgent:
    def __init__(self):
        # self.llm = init_langchain_chat_openai()
        self.memory = MemorySaver()

    def build_graph(self) -> CompiledStateGraph:
        builder = StateGraph(
            state_schema=FailureAnalysisState, output_schema=FailureAnalysisOutputState
        )
        builder.add_node("get_failures", get_failures)
        builder.add_node("generate_failures_summary", generate_failures_summary)
        builder.add_edge(START, "get_failures")
        builder.add_edge("get_failures", "generate_failures_summary")
        builder.add_edge("generate_failures_summary", END)
        graph = builder.compile()
        # save_graph_image(graph, "simple_failure_analysis_agent.png")
        return graph


# Summarization subgraph
class QuestionSummarizationState(TypedDict):
    cleaned_logs: List[Log]
    qs_summary: str
    report: str
    processed_logs: List[str]


class QuestionSummarizationOutputState(TypedDict):
    report: str
    processed_logs: List[str]


def generate_question_summary(state:QuestionSummarizationState):
    cleaned_logs = state["cleaned_logs"]
    # Add fxn: summary = summarize(generate_summary)
    summary = "Questions focused on usage of ChatOllama and Chroma vector store."
    return {
        "qs_summary": summary,
        "processed_logs": [f"summary-on-log-{log['id']}" for log in cleaned_logs],
    }


def send_to_slack(state:QuestionSummarizationState):
    qs_summary = state["qs_summary"]
    # Add fxn: report = report_generation(qs_summary)
    report = "foo bar baz"
    return {"report": report}


class QuestionSummarizationAgent:
    def __init__(self):
        # self.llm = init_langchain_chat_openai()
        self.memory = MemorySaver()

    def build_graph(self) -> CompiledStateGraph:
        builder = StateGraph(
            state_schema=QuestionSummarizationState,
            output_schema=QuestionSummarizationOutputState,
        )
        builder.add_node("generate_question_summary", generate_question_summary)
        builder.add_node("send_to_slack", send_to_slack)

        builder.add_edge(START, "generate_question_summary")
        builder.add_edge("generate_question_summary", "send_to_slack")
        builder.add_edge("send_to_slack", END)
        graph = builder.compile()
        return graph


# Entry Graph
class EntryGraphState(TypedDict):
    raw_logs: List[Log]
    cleaned_logs: List[Log]

    fa_summary: str  # This will only be generated in the FA sub-graph
    report: str  # This will only be generated in the QS sub-graph
    processed_logs: Annotated[
        List[str], add
    ]  # This will be generated in BOTH sub-graphs


def clean_logs(state):
    # Get logs
    raw_logs = state["raw_logs"]
    # Data cleaning raw_logs -> docs
    cleaned_logs = raw_logs
    return {"cleaned_logs": cleaned_logs}


class LogAnalysisAgent:
    def __init__(self):
        # self.llm = init_langchain_chat_openai()
        self.memory = MemorySaver()

    def build_graph(self) -> CompiledStateGraph:
        builder = StateGraph(EntryGraphState)

        builder.add_node("clean_logs", clean_logs)
        builder.add_node("failure_analysis", FailureAnalysisAgent().build_graph())
        builder.add_node(
            "question_summarization", QuestionSummarizationAgent().build_graph()
        )

        builder.add_edge(START, "clean_logs")
        builder.add_edge("clean_logs", "failure_analysis")
        builder.add_edge("clean_logs", "question_summarization")
        builder.add_edge(["failure_analysis", "question_summarization"], END)

        graph = builder.compile()
        
        save_graph_image(graph, "log_analysis_agent.png")
        return graph

    def run(self):
        graph = self.build_graph()
        
        # Dummy logs
        question_answer = Log(
            id="1",
            question="How can I import ChatOllama?",
            answer="To import ChatOllama, use: 'from langchain_community.chat_models import ChatOllama.'",
        )

        question_answer_feedback = Log(
            id="2",
            question="How can I use Chroma vector store?",
            answer="To use Chroma, define: rag_chain = create_retrieval_chain(retriever, question_answer_chain).",
            grade=0,
            grader="Document Relevance Recall",
            feedback="The retrieved documents discuss vector stores in general, but not Chroma specifically",
        )

        raw_logs = [question_answer,question_answer_feedback]
        output = graph.invoke({"raw_logs": raw_logs})
        print(output)


if __name__ == "__main__":
    # agent = SimpleNodeAgent()
    # agent.run()

    # agent = SimpleMuiltiAgent()
    # agent.run()
    
    
    agent = LogAnalysisAgent()
    agent.run()
    
