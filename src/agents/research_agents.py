"""
https://github.com/langchain-ai/langchain-academy/blob/main/module-4/research-assistant.ipynb

Goal
Our goal is to build a lightweight, multi-agent system around chat models that customizes the research process.

Source Selection
- Users can choose any set of input sources for their research.

Planning
- Users provide a topic, and the system generates a team of AI analysts, each focusing on one sub-topic.
- Human-in-the-loop will be used to refine these sub-topics before research begins.

LLM Utilization
- Each analyst will conduct in-depth interviews with an expert AI using the selected sources.
- The interview will be a multi-turn conversation to extract detailed insights as shown in the STORM paper.
  Assisting in Writing Wikipedia-like Articles From Scratch with Large Language Models](https://arxiv.org/abs/2402.14207)
- These interviews will be captured in a using sub-graphs with their internal state.


Research Process
- Experts will gather information to answer analyst questions in parallel.
- And all interviews will be conducted simultaneously through map-reduce.


Output Format
- The gathered insights from each interview will be synthesized into a final report.
- We'll use customizable prompts for the report, allowing for a flexible output format.


"""

from concurrent.futures import thread
from logging import config
from typing import List, Dict, Text, Annotated, TypedDict, Literal
import operator
from pydantic import Field, BaseModel  # updated since filming

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
from langchain_tavily import TavilySearch
from langchain_community.document_loaders import WikipediaLoader
from langchain_core.messages import get_buffer_string
from langgraph.types import Send  # updated in 1.0

from utils.env_utils import load_env
from utils.qwen_api import init_langchain_chat_openai
from utils.langchain_utils import save_graph_image


class SearchState(TypedDict):
    question: str
    answer: str
    context: Annotated[list, operator.add]


def search_web(state: SearchState):
    """Retrieve docs from web search"""
    # Search
    tavily_search = TavilySearch(max_results=3)
    question = state["question"]
    data = tavily_search.invoke({"query": question})
    # search_docs = data.get("results", data)
    
    #  # Format
    # formatted_search_docs = "\n\n---\n\n".join(
    #     [
    #         f'<Document href="{doc["url"]}"/>\n{doc["content"]}\n</Document>'
    #         for doc in search_docs
    #     ]
    # )
    
    
    # Handle different return types from TavilySearch
    if isinstance(data, list):
        search_docs = data
    elif isinstance(data, dict) and "results" in data:
        search_docs = data["results"]
    else:
        # Fallback if unexpected format
        search_docs = []

    # Format
    formatted_search_docs = "\n\n---\n\n".join(
        [
            f'<Document href="{doc.get("url", "N/A")}">\n{doc.get("content", "N/A")}\n</Document>'
            for doc in search_docs
            if isinstance(doc, dict)
        ]
    )

    return {"context": [formatted_search_docs]}


def search_wikipedia(state: SearchState):
    """Retrieve docs from wikipedia"""

    # Search
    search_docs = WikipediaLoader(query=state["question"], load_max_docs=2).load()

    # Format
    formatted_search_docs = "\n\n---\n\n".join(
        [
            f'<Document source="{doc.metadata["source"]}" page="{doc.metadata.get("page", "")}">\n{doc.page_content}\n</Document>'
            for doc in search_docs
        ]
    )

    return {"context": [formatted_search_docs]}


class SimpleResearchAgent:
    def __init__(self):

        self.tools = []
        self.llm = init_langchain_chat_openai()
        self.memory = MemorySaver()

    def generate_answer(self, state):
        """Node to answer a question"""

        # Get state
        context = state["context"]
        question = state["question"]

        # Template
        answer_template = (
            """Answer the question {question} using this context: {context}"""
        )
        answer_instructions = answer_template.format(question=question, context=context)

        # Answer
        answer = self.llm.invoke(
            [SystemMessage(content=answer_instructions)]
            + [HumanMessage(content=f"Answer the question.")]
        )

        # Append it to state
        return {"answer": answer}

    def build_graph(self) -> CompiledStateGraph:
        builder = StateGraph(SearchState)

        # Initialize each node with node_secret
        builder.add_node("search_web", search_web)
        builder.add_node("search_wikipedia", search_wikipedia)
        builder.add_node("generate_answer", self.generate_answer)

        # Flow
        builder.add_edge(START, "search_wikipedia")
        builder.add_edge(START, "search_web")
        builder.add_edge("search_wikipedia", "generate_answer")
        builder.add_edge("search_web", "generate_answer")
        builder.add_edge("generate_answer", END)
        graph = builder.compile()

        save_graph_image(graph, "research_agent_v1.png")
        return graph

    def run(self, question: str = "How were Nvidia's Q2 2025 earnings") -> str:
        """Run the agent"""
        graph = self.build_graph()
        # Run
        state = graph.invoke({"question": question})

        # Return
        return state["answer"]


class Analyst(BaseModel):
    affiliation: str = Field(description="The Primary affiliation of the analyst")
    name: str = Field(description="The name of the analyst")
    role: str = Field(description="The role of the analyst in the context of the topic")
    description: str = Field(
        description="The description of the analyst focus, concerns and motives"
    )

    @property
    def persona(self) -> str:
        """Return the persona of the analyst"""
        return f"Name: {self.name}\nRole: {self.role}\nAffiliation: {self.affiliation}\nDescription: {self.description}\n"


class Perspectives(BaseModel):
    """The perspective of the agent"""

    analysts: List[Analyst] = Field(
        description="Comprehensive list of analysts with their roles and affiliations."
    )


class GenerateAnalystState(TypedDict):
    """The state of the generate analyst state"""

    topic: str = Field(description="The topic of the research")
    max_analysts: int = Field(description="The maximum number of analysts to generate")
    human_analyst_feedback: str = Field(
        description="Feedback from the human on the analysts"
    )
    analysts: List[Analyst] = Field(description="analyst asking questions")


# Part2: Conduct Interview
class InterviewState(MessagesState):
    """The state of the interview state"""


    analyst: Analyst = Field(description="The analyst asking questions")
    max_num_turns: int = Field(
        description="The maximum number of conversation in the interview"
    )
    
    context: Annotated[list, operator.add] = Field(
        description="The source docs of the interview"
    )
    
    interview: str = Field(description="The interview transcript")
    sections: list[str] = Field(
        description="Final key we duplicate in outer state for Send() API"
    )


class SearchQuery(BaseModel):
    search_query: str = Field(description="Search query for retrieval.")


class ReasearchState(TypedDict):
    topic: str = Field(description="The topic we are searching for")
    max_analysts: int = Field(description="Max number of analysts to search for")
    human_analyst_feedback: str = Field(
        description="Feedback from human analyst on search results"
    )
    analysts: List[Analyst] = Field(description="List of analysts found")
    sections: Annotated[list, operator.add] = Field(
        description="List of sections found"
    )
    introduction: str = Field(description="Introduction for the final report")
    content: str = Field(description="Content for the final report")
    conclusion: str = Field(description="Conclusion for the final report")
    final_report: str = Field(description="Final report")


class ReaserchAgent:
    def __init__(self):
        self.analyst_instructions = self.get_analyst_instruct()
        self.question_instructions = self.get_question_instructions()
        self.search_instructions = self.get_search_instructions()
        self.answer_instructions = self.get_answer_instructions()
        self.section_writer_instructions = self.get_section_writer_instructions()
        self.report_writer_instructions = self.get_report_writer_instructions()
        self.intro_conclusion_instructions = self.get_intro_conclusion_instructions()

        self.llm = init_langchain_chat_openai()

        self.memory = MemorySaver()

        self.tavily_search = TavilySearch(max_results=3)

    def get_analyst_instruct(
        self,
    ) -> str:
        analyst_instructions = """You are tasked with creating a set of AI analyst personas. Follow these instructions carefully:

        1. First, review the research topic:
        {topic}
                
        2. Examine any editorial feedback that has been optionally provided to guide creation of the analysts: 
                
        {human_analyst_feedback}
            
        3. Determine the most interesting themes based upon documents and / or feedback above.
                            
        4. Pick the top {max_analysts} themes.

        5. Assign one analyst to each theme."""
        return analyst_instructions

    def create_analysts(self, state: GenerateAnalystState) -> List[Analyst]:
        """Node to generate analysts"""

        # Get state
        topic = state["topic"]
        max_analysts = state["max_analysts"]
        human_analyst_feedback = state.get("human_analyst_feedback", "")

        # Enforce structured output
        structured_llm = self.llm.with_structured_output(Perspectives)
        system_message = self.analyst_instructions.format(
            topic=topic,
            human_analyst_feedback=human_analyst_feedback,
            max_analysts=max_analysts,
        )

        perpectives = structured_llm.invoke(
            [system_message] + [HumanMessage(content=f"Generate the set of analysts")]
        )

        return {"analysts": perpectives.analysts}

    def human_feedback(self, state: GenerateAnalystState) -> str:
        """"""
        pass

    def should_continue(
        self, state: GenerateAnalystState
    ) -> Literal["create_analysts", END]:
        human_analyst_feedback = state.get("human_analyst_feedback", None)
        if human_analyst_feedback:
            return "create_analysts"
        return END

    def build_analysts_graph(self) -> CompiledStateGraph:
        builder = StateGraph(GenerateAnalystState)
        builder.add_node("create_analysts", self.create_analysts)
        builder.add_node("human_feedback", self.human_feedback)

        builder.add_edge(START, "create_analysts")
        builder.add_edge("create_analysts", "human_feedback")
        builder.add_conditional_edges(
            "human_feedback", self.should_continue, ["create_analysts", END]
        )

        graph = builder.compile(
            checkpointer=self.memory, interrupt_before=["human_feedback"]
        )
        save_graph_image(graph, filename="research_agent_analysts.png")

        return graph

    def _generate_analysts(
        self, graph, values, config: dict
    ) -> List[str]:
        """Get analysts from the state"""
        # Run the graph until the first interruption
        for event in graph.stream(values,
            config=config,
            stream_mode="values",
        ):
            analysts = event.get("analysts", "")
            if analysts:
                for analyst in analysts:
                    print(f"Name: {analyst.name}")
                    print(f"Affiliation: {analyst.affiliation}")
                    print(f"Role: {analyst.role}")
                    print(f"Description: {analyst.description}")
                    print("-" * 50)
                return analysts
        return None

    def run_generating_analysts_with_hitp(self, topic: str) -> GenerateAnalystState:
        graph = self.build_analysts_graph()
        max_analysts = 3
        config = {"configurable": {"thread_id": "t001"}}
        
        initial_values = {
                "max_analysts": max_analysts,
                "topic": topic,
                "tool_loop_count": 0,
            }

        # Run the graph until interruption and get analysts from state
        analysts = self._generate_analysts(graph,initial_values,  config)

        # get the state and look at next node
        state = graph.get_state(config=config)
        print(f"Next Node: {state.next}")
        
        # We now update the state as if we are the human_feedback node
        checkpoint = graph.update_state(
            config=config,
            values={
                "human_analyst_feedback": "Add in someone from a startup to add an entrepreneur perspective"
            },
            as_node="human_feedback",
        )
        print(f"Checkpoint: {checkpoint}")

        # continue the graph execution
        analysts = self._generate_analysts(graph, values=None, config=config)

        # if we are satisfied,
        further_feedback = None
        checkpoint = graph.update_state(
            config=config,
            values={"human_analyst_feedback": further_feedback},
            as_node="human_feedback",
        )
        print(f"Checkpoint: {checkpoint}")

        # continue the graph execution to end
        for event in graph.stream(None, config, stream_mode="values"):
            print("---Node----")
            node_name = next(iter(event.keys()))
            print(f"Node: {node_name}")

        final_state = graph.get_state(config)
        analysts = final_state.values.get("analysts")
        print(f"{final_state.next}")

        for analyst in analysts:
            print(f"Name: {analyst.name}")
            print(f"Affiliation: {analyst.affiliation}")
            print(f"Role: {analyst.role}")
            print(f"Description: {analyst.description}")
            print("-" * 50)
        
        return final_state

    def get_question_instructions(self) -> str:
        """"""
        question_instructions = """You are an analyst tasked with interviewing an expert to learn about a specific topic. 

        Your goal is boil down to interesting and specific insights related to your topic.

        1. Interesting: Insights that people will find surprising or non-obvious.
                
        2. Specific: Insights that avoid generalities and include specific examples from the expert.

        Here is your topic of focus and set of goals: {goals}
                
        Begin by introducing yourself using a name that fits your persona, and then ask your question.

        Continue to ask questions to drill down and refine your understanding of the topic.
                
        When you are satisfied with your understanding, complete the interview with: "Thank you so much for your help!"

        Remember to stay in character throughout your response, reflecting the persona and goals provided to you."""
        return question_instructions

    def generate_question(self, state: InterviewState):
        """Node to generate questions"""
        analyst = state["analyst"]
        messages = state["messages"]

        system_message = self.question_instructions.format(goals=analyst.persona)
        question = self.llm.invoke([SystemMessage(content=system_message)] + messages)
        return {"messages": [question]}

    def get_search_instructions(self) -> SystemMessage:
        # Search query writing
        search_instructions = SystemMessage(
            content=f"""You will be given a conversation between an analyst and an expert. 

        Your goal is to generate a well-structured query for use in retrieval and / or web-search related to the conversation.
                
        First, analyze the full conversation.

        Pay particular attention to the final question posed by the analyst.

        Convert this final question into a well-structured web search query"""
        )
        return search_instructions

    def search_web(self, state: InterviewState):
        """Node to Retrieve docs from web search"""

        # generate a search query
        structured_llm = self.llm.with_structured_output(SearchQuery)
        search_query = structured_llm.invoke(
            [self.search_instructions] + state["messages"]
        )

        # Ensure we have a valid search query
        query = getattr(search_query, 'search_query', str(search_query))
        if not query or not isinstance(query, str):
            query = "general information"  # fallback query

        # execute the search
        try:
            data = self.tavily_search.invoke({"query": query})
        except Exception as e:
            # If search fails, return empty context
            return {"context": ["Search failed: " + str(e)]}
        
        # Handle different return types from TavilySearch
        if isinstance(data, list):
            search_docs = data
        elif isinstance(data, dict) and "results" in data:
            search_docs = data["results"]
        else:
            # Fallback if unexpected format
            search_docs = []

        # format the search docs
        formatted_search_docs = "\n\n---\n\n".join(
            [
                f'<Document href="{doc.get("url", "N/A")}">\n{doc.get("content", "N/A")}\n</Document>'
                for doc in search_docs
                if isinstance(doc, dict)
            ]
        )
        return {"context": [formatted_search_docs]}

    def search_wikipedia(self, state: InterviewState):
        """Retrieve docs from wikipedia"""
        structed_llm = self.llm.with_structured_output(SearchQuery)

        search_query = structed_llm.invoke(
            [self.search_instructions] + state["messages"]
        )

        search_docs = WikipediaLoader(
            query=search_query.search_query, load_max_docs=2
        ).load()

        formatted_search_docs = "\n\n---\n\n".join(
            [
                f'<Document source="{doc.metadata["source"]}" page="{doc.metadata.get("page", "")}">\n{doc.page_content}\n</Document>'
                for doc in search_docs
            ]
        )

        return {"context": [formatted_search_docs]}

    def get_answer_instructions(self) -> str:
        answer_instructions = """You are an expert being interviewed by an analyst.

        Here is analyst area of focus: {goals}. 
                
        You goal is to answer a question posed by the interviewer.

        To answer question, use this context:
                
        {context}

        When answering questions, follow these guidelines:
                
        1. Use only the information provided in the context. 
                
        2. Do not introduce external information or make assumptions beyond what is explicitly stated in the context.

        3. The context contain sources at the topic of each individual document.

        4. Include these sources your answer next to any relevant statements. For example, for source # 1 use [1]. 

        5. List your sources in order at the bottom of your answer. [1] Source 1, [2] Source 2, etc
                
        6. If the source is: <Document source="assistant/docs/llama3_1.pdf" page="7"/>' then just list: 
                
        [1] assistant/docs/llama3_1.pdf, page 7 
                
        And skip the addition of the brackets as well as the Document source preamble in your citation."""
        return answer_instructions

    def generate_answer(self, state: InterviewState) -> str:
        """Node to answer the question"""

        analyst = state["analyst"]
        messages = state["messages"]
        context = state["context"]

        system_message = self.answer_instructions.format(
            goals=analyst.persona, context=context
        )
        answer = self.llm.invoke([system_message] + messages)

        answer.name = "expert"

        return {"messages": [answer]}

    def save_interview(self, state: InterviewState):
        messages = state["messages"]
        interview = get_buffer_string(messages)

        return {"interview": interview}

    def route_message(self, state: InterviewState, name: str = "expert")->Literal["ask_question", "save_interview"]:
        """route between question and answer"""
        messages = state["messages"]
        max_num_turns = state.get("max_num_turns", 2)

        num_response = len(
            [m for m in messages if isinstance(m, AIMessage) and m.name == name]
        )

        if num_response >= max_num_turns:
            return "save_interview"

        last_question = messages[-2]

        if "Thank you so much for your help" in last_question.content:
            return "save_interview"
        return "ask_question"

    def get_section_writer_instructions(self):
        section_writer_instructions = """You are an expert technical writer. 
            
        Your task is to create a short, easily digestible section of a report based on a set of source documents.

        1. Analyze the content of the source documents: 
        - The name of each source document is at the start of the document, with the <Document tag.
                
        2. Create a report structure using markdown formatting:
        - Use ## for the section title
        - Use ### for sub-section headers
                
        3. Write the report following this structure:
        a. Title (## header)
        b. Summary (### header)
        c. Sources (### header)

        4. Make your title engaging based upon the focus area of the analyst: 
        {focus}

        5. For the summary section:
        - Set up summary with general background / context related to the focus area of the analyst
        - Emphasize what is novel, interesting, or surprising about insights gathered from the interview
        - Create a numbered list of source documents, as you use them
        - Do not mention the names of interviewers or experts
        - Aim for approximately 400 words maximum
        - Use numbered sources in your report (e.g., [1], [2]) based on information from source documents
                
        6. In the Sources section:
        - Include all sources used in your report
        - Provide full links to relevant websites or specific document paths
        - Separate each source by a newline. Use two spaces at the end of each line to create a newline in Markdown.
        - It will look like:

        ### Sources
        [1] Link or Document name
        [2] Link or Document name

        7. Be sure to combine sources. For example this is not correct:

        [3] https://ai.meta.com/blog/meta-llama-3-1/
        [4] https://ai.meta.com/blog/meta-llama-3-1/

        There should be no redundant sources. It should simply be:

        [3] https://ai.meta.com/blog/meta-llama-3-1/
                
        8. Final review:
        - Ensure the report follows the required structure
        - Include no preamble before the title of the report
        - Check that all guidelines have been followed"""

        return section_writer_instructions

    def write_section(self, state: InterviewState):
        """Node to answer a question:
        TODO: not use interverview"""
        interview = state["interview"]
        context = state["context"]
        analyst = state["analyst"]
        system_message = self.section_writer_instructions.format(
            focus=analyst.description
        )
        section = self.llm.invoke(
            [SystemMessage(content=system_message)]
            + [
                HumanMessage(
                    content=f"Use this source to write your section: {context}"
                )
            ]
        )
        return {"sections": [section.content]}

    def build_interview_graph(self):
        builder = StateGraph(InterviewState)
        builder.add_node("ask_question", self.generate_question)
        builder.add_node("search_web", self.search_web)
        builder.add_node("search_wikipedia", self.search_wikipedia)
        builder.add_node("answer_question", self.generate_answer)
        builder.add_node("save_interview", self.save_interview)
        builder.add_node("write_section", self.write_section)

        builder.add_edge(START, "ask_question")
        builder.add_edge("ask_question", "search_web")
        builder.add_edge("ask_question", "search_wikipedia")
        builder.add_edge("search_web", "answer_question")
        builder.add_edge("search_wikipedia", "answer_question")
        builder.add_conditional_edges(
            "answer_question", self.route_message, ["ask_question", "save_interview"]
        )
        builder.add_edge("save_interview", "write_section")
        builder.add_edge("write_section", END)

        interview_graph = builder.compile(checkpointer=self.memory).with_config(
            run_name="Conduct Interview"
        )
        save_graph_image(interview_graph, filename="research_agent_interview.png")
        return interview_graph

    def run_interview(self, topic) -> None:
        analyst = Analyst(
            affiliation="Tech Innovators Inc.",
            name="Alex Johnson",
            role="Startup Entrepreneur",
            description="Alex is a co-founder of a tech startup that focuses on developing innovative AI solutions. With a keen interest in leveraging cutting-edge technologies to gain a competitive edge, Alex is particularly interested in how adopting LangGraph as an agent framework can streamline development processes, reduce costs, and accelerate time-to-market for new AI products.",
        )

        interview_graph = self.build_interview_graph()

        config = {"configurable": {"thread_id": "t001"}}
        messages = [
            HumanMessage(f"So you said you were writing an article on {topic}?")
        ]
        interview = interview_graph.invoke(
            {"analyst": analyst, "messages": messages, "max_num_turns":2}, config=config
        )
        print(interview["sections"][0])
        return interview

    def initiate_all_interview(self, state: ReasearchState)->Literal["conduct_interview", "create_analysts"]:
        """This is the "map" step where we run each interview sub-graph using Send API"""
        human_analyst_feedback = state["human_analyst_feedback"]
        if human_analyst_feedback:
            return "create_analysts"
        else:
            topic = state["topic"]
            tasks = [
                Send(
                    node="conduct_interview",
                    arg={
                        "analyst": analyst,
                        "messages": [
                            HumanMessage(
                                f"So you said you were writing an article on {topic}"
                            )
                        ],
                    },
                )
                for analyst in state["analysts"]
            ]
            return tasks

    def get_report_writer_instructions(self):
        report_writer_instructions = """You are a technical writer creating a report on this overall topic: 

        {topic}
            
        You have a team of analysts. Each analyst has done two things: 

        1. They conducted an interview with an expert on a specific sub-topic.
        2. They write up their finding into a memo.

        Your task: 

        1. You will be given a collection of memos from your analysts.
        2. Think carefully about the insights from each memo.
        3. Consolidate these into a crisp overall summary that ties together the central ideas from all of the memos. 
        4. Summarize the central points in each memo into a cohesive single narrative.

        To format your report:
        
        1. Use markdown formatting. 
        2. Include no pre-amble for the report.
        3. Use no sub-heading. 
        4. Start your report with a single title header: ## Insights
        5. Do not mention any analyst names in your report.
        6. Preserve any citations in the memos, which will be annotated in brackets, for example [1] or [2].
        7. Create a final, consolidated list of sources and add to a Sources section with the `## Sources` header.
        8. List your sources in order and do not repeat.

        [1] Source 1
        [2] Source 2

        Here are the memos from your analysts to build your report from: 

        {context}"""

        return report_writer_instructions

    def get_intro_conclusion_instructions(self):
        intro_conclusion_instructions = """You are a technical writer finishing a report on {topic}

        You will be given all of the sections of the report.

        You job is to write a crisp and compelling introduction or conclusion section.

        The user will instruct you whether to write the introduction or conclusion.

        Include no pre-amble for either section.

        Target around 100 words, crisply previewing (for introduction) or recapping (for conclusion) all of the sections of the report.

        Use markdown formatting. 

        For your introduction, create a compelling title and use the # header for the title.

        For your introduction, use ## Introduction as the section header. 

        For your conclusion, use ## Conclusion as the section header.

        Here are the sections to reflect on for writing: {formatted_str_sections}"""
        return intro_conclusion_instructions

    def write_report(self, state: ReasearchState) -> Dict[str, str]:

        sections = state["sections"]
        topic = state["topic"]

        formated_str_sections = "\n\n".join([f"{section}" for section in sections])

        system_message = self.report_writer_instructions.format(
            context=formated_str_sections, topic=topic
        )

        report = self.llm.invoke(
            [SystemMessage(content=system_message)]
            + [HumanMessage(content=f"Write a report based upon these memos.")]
        )
        return {"content": report.content}

    def write_introduction(self, state: ReasearchState) -> Dict[str, str]:
        sections = state["sections"]
        topic = state["topic"]

        formated_str_sections = "\n\n".join([f"{section}" for section in sections])

        instructions = self.intro_conclusion_instructions.format(
            topic=topic, formatted_str_sections=formated_str_sections
        )
        intro = self.llm.invoke(
            [SystemMessage(content=instructions)]   + [HumanMessage(content=f"Write the report introduction")]
        )
        return {"introduction": intro.content}

    def write_conclusion(self, state: ReasearchState) -> Dict[str, str]:
        sections = state["sections"]
        topic = state["topic"]

        formated_str_sections = "\n\n".join([f"{section}" for section in sections])

        instructions = self.intro_conclusion_instructions.format(
            topic=topic, formatted_str_sections=formated_str_sections
        )
        conclustion = self.llm.invoke(
            [SystemMessage(content=instructions)]
            + [HumanMessage(content=f"Write the report conclusion")]
        )
        return {"conclusion": conclustion.content}

    def finalize_report(self, state: ReasearchState):
        """The is the "reduce" step where we gather all the sections, combine them, and reflect on them to write the intro/conclusion"""
        content = state["content"]
        if content.startswith("## Insights"):
            content = content.strip("## Insights")
        if "## Sources" in content:
            try:
                content, sources = content.split("## Sources")
            except:
                sources = None
        else:
            sources = None

        final_report = (
            state["introduction"]
            + "\n\n---\n\n"
            + content
            + "\n\n---\n\n"
            + state["conclusion"]
        )
        if sources is not None:
            final_report += "\n\n## Sources\n\n" + sources
        return {"final_report": final_report}

    def build_overall_graph(self) -> CompiledStateGraph:
        builder = StateGraph(ReasearchState)
        builder.add_node("create_analysts", self.create_analysts)
        builder.add_node("human_feedback", self.human_feedback)
        builder.add_node("conduct_interview", self.build_interview_graph())
        builder.add_node("write_report", self.write_report)
        builder.add_node("write_introduction", self.write_introduction)
        builder.add_node("write_conclusion", self.write_conclusion)
        builder.add_node("finalize_report", self.finalize_report)

        builder.add_edge(START, "create_analysts")
        builder.add_edge("create_analysts", "human_feedback")
        builder.add_conditional_edges(
            "human_feedback",
            self.initiate_all_interview,
            ["create_analysts", "conduct_interview"],
        )
        builder.add_edge("conduct_interview", "write_report")
        builder.add_edge("conduct_interview", "write_introduction")
        builder.add_edge("conduct_interview", "write_conclusion")
        builder.add_edge(
            ["write_report", "write_introduction", "write_conclusion"],
            "finalize_report",
        )
        builder.add_edge("finalize_report", END)

        graph = builder.compile(
            checkpointer=self.memory, interrupt_before=["human_feedback"]
        )
        save_graph_image(graph, filename="research_agent_overall.png")
        return graph

    def run_reaserch_agent(self,topic):
        graph = self.build_overall_graph()
        # Inputs
        max_analysts = 3
        
        thread = {"configurable": {"thread_id": "1"}}

        # Run the graph until the first interruption
        values = {"topic": topic, "max_analysts": max_analysts}
        analysts = self._generate_analysts(graph=graph, values=values, config=thread)
        
        # We now update the state as if we are the human_feedback node
        hitl_check_point = graph.update_state(thread, {"human_analyst_feedback": 
                                        "Add in the CEO of gen ai native startup"}, as_node="human_feedback")
        
        # continue the graph execution
        analysts = self._generate_analysts(graph=graph, values=None,config=thread)
        
        # Confirm we are happy
        satisfied_check_point= graph.update_state(thread, {"human_analyst_feedback": None}, as_node="human_feedback")
        
        # Continue
        for event in graph.stream(None, thread, stream_mode="updates"):
            print("--Node--")
            node_name = next(iter(event.keys()))
            print(node_name)
        
        final_state = graph.get_state(thread)
        report = final_state.values.get('final_report')
        return report
                    
        


if __name__ == "__main__":

    load_env()
    # agent = SimpleResearchAgent()
    # print(agent.run())

    agent = ReaserchAgent()
    
    topic = "The benefits of adopting LangGraph as an agent framework"
    # agent.run_generating_analysts_with_hitp(topic=topic)
    # agent.run_interview(topic)
    agent.run_reaserch_agent(topic)
