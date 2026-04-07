from typing import Annotated, List, Literal, Union, NotRequired
from langchain.chat_models import init_chat_model
from langchain_community.chat_models import ChatTongyi
from langchain.agents import create_agent 
from langchain.agents import AgentState
from langgraph.types import Command
from langchain_core.tools import InjectedToolCallId, tool
from utils.env_utils import load_env, get_env
from utils.format_utils import format_messages
from utils.qwen_api import init_openai_client_with_qwen,init_langchain_chat_tongyi
from prompts.deep_agent_prompts import SYSTEM_PROMPT, TODO_USAGE_INSTRUCTIONS, SIMPLE_RESEARCH_INSTRUCTIONS
from deep_agents.deep_agent_states import CalcState, DeepAgentState
from tools.calculator_tools import calculator, calculator_wstate
from tools.todo_tools import write_todos, read_todos
from tools.web_search_tools import web_search



load_env()




class DeepAgentExecutor:
  def __init__(self,model_name ="qwen-plus"):
    self.model_name = model_name
    self.model = self.init_llm(model_name)
    self.system_prompt = self.build_system_prompt()
    self.state_schema =  self.build_state_schema()
    self.tools =  self.build_tools()


  def build_system_prompt(self):
      # system_prompt = SYSTEM_PROMPT
      system_prompt=TODO_USAGE_INSTRUCTIONS + "\n\n"  + "=" * 80  + "\n\n"  + SIMPLE_RESEARCH_INSTRUCTIONS,
      return system_prompt
  
  def build_state_schema(self):
      state_schema = DeepAgentState
      return state_schema
    
  
  def build_tools(self)->List[tool]:
      # tools  = self._build_calculator_tools()
      tools = [write_todos, web_search, read_todos]
      return tools
   
    
  def _build_calculator_tools(self)->List[tool]:
      # tools  = [calculator]
      tools  = [calculator_wstate]
      return tools

  def init_llm(self, model_name: str="qwen-plus", llm_kwargs: dict = None):
     if model_name.startswith("qwen"):
        model = init_langchain_chat_tongyi(model_name=model_name)
     else:
        model = init_chat_model(model_name, llm_kwargs)
     return model

  def create_calculator_agent(self,):
      # Create agent using create_agent directly
      system_prompt = SYSTEM_PROMPT
      model = self.model
      tools = self._build_calculator_tools()
      
      # state_schema=AgentState,  # default
      state_schema =  CalcState

      # Create agent
      agent = create_agent(             # updated for 1.0
          model,
          tools,
          system_prompt=system_prompt,  # updated
          state_schema=state_schema,
      ).with_config({"recursion_limit": 20})  
      return agent
  
  def create_react_agent(self,):
      # Create agent using create_agent directly
      system_prompt = self.system_prompt
      model = self.model
      tools = self.tools
      state_schema = self.state_schema

      # Create agent
      agent = create_agent(             # updated for 1.0
          model,
          tools,
          system_prompt=system_prompt,  # updated for 1.0
          state_schema=state_schema,
         
      ).with_config({"recursion_limit": 20})  #recursion_limit limits the number of steps the agent will run
      return agent
  
  def run_calculator(self, query: str):
      # Example usage
      messages =  [
                    {
                        "role": "user", "content":query ,
                    }
                ]

      agent = self.create_calculator_agent()

      result = agent.invoke({"messages":messages})

      print(f"result keys:{result.keys()}")
      messages = result["messages"]
      format_messages(messages) 
      operations = result.get("ops")
      print(f"operations: {operations}")
      return result

  
  def run(self, query: str, todos: List[str] = []):
      # Example usage
      messages =  [
                    {
                        "role": "user", "content":query ,
                    }
                ]

      agent = self.create_react_agent()
  
      result = agent.invoke({"messages":messages,"todos":todos})

      print(f"result keys:{result.keys()}")
      messages = result["messages"]
      format_messages(messages) 
      operations = result.get("ops")
      print(f"operations: {operations}")
      return result



if __name__ == "__main__":
  load_env()

  deep_agent_executor = DeepAgentExecutor()
  
  query ="What is 3.1 * 4.2?"
  query = "What is 3.1 * 4.2 + 5.5 * 6.5?"
  result = deep_agent_executor.run_calculator(query=query)


  query ="Give me a short summary of the Model Context Protocol (MCP)."
  todos = []
  result = deep_agent_executor.run(query=query,todos= todos)

  print(result)

