
"""
https://help.aliyun.com/zh/model-studio/models
pip install langchain-community dashscope

"""
import os
import time
from pathlib import Path
from openai import OpenAI
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.chat_models import ChatTongyi
from langchain_openai import ChatOpenAI

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chat_models import init_chat_model
from utils.openai_apis import call_openai_client_parse,call_openai_client_create,call_openai_client
from utils.env_utils import load_env, get_env


DASHSCOPE_BASE_URL= "https://dashscope.aliyuncs.com/compatible-mode/v1" 

ENDPOINT =  '/v1/chat/completions'

QWEN3_MAX = "qwen3-max"
QWEN_PLUS = "qwen-plus"
QWEN_FLASH = "qwen-flash"




def upload_file(file_path):
    print(f"正在上传包含请求信息的JSONL文件...")
    file_object = qwen_client.files.create(file=Path(file_path), purpose="batch")
    print(f"文件上传成功。得到文件ID: {file_object.id}\n")
    return file_object.id

def create_batch_job(input_file_id):
    print(f"正在基于文件ID，创建Batch任务...")
    # 请注意:此处endpoint参数值需和输入文件中的url字段保持一致.测试模型(batch-test-model)填写/v1/chat/ds-test,Embedding文本向量模型填写/v1/embeddings,其他模型填写/v1/chat/completions
    batch = qwen_client.batches.create(input_file_id=input_file_id, endpoint=ENDPOINT, completion_window="24h")
    print(f"Batch任务创建完成。 得到Batch任务ID: {batch.id}\n")
    return batch.id

def check_job_status(batch_id):
    print(f"正在检查Batch任务状态...")
    batch = qwen_client.batches.retrieve(batch_id=batch_id)
    print(f"Batch任务状态: {batch.status}\n")
    return batch.status

def get_output_id(batch_id):
    print(f"正在获取Batch任务中执行成功请求的输出文件ID...")
    batch = qwen_client.batches.retrieve(batch_id=batch_id)
    print(f"输出文件ID: {batch.output_file_id}\n")
    return batch.output_file_id

def get_error_id(batch_id):
    print(f"正在获取Batch任务中执行错误请求的输出文件ID...")
    batch = qwen_client.batches.retrieve(batch_id=batch_id)
    print(f"错误文件ID: {batch.error_file_id}\n")
    return batch.error_file_id

def download_results(output_file_id, output_file_path):
    print(f"正在打印并下载Batch任务的请求成功结果...")
    content = qwen_client.files.content(output_file_id)
    # 打印部分内容以供测试
    print(f"打印请求成功结果的前1000个字符内容: {content.text[:1000]}...\n")
    # 保存结果文件至本地
    content.write_to_file(output_file_path)
    print(f"完整的输出结果已保存至本地输出文件result.jsonl\n")

def download_errors(error_file_id, error_file_path):
    print(f"正在打印并下载Batch任务的请求失败信息...")
    content = qwen_client.files.content(error_file_id)
    # 打印部分内容以供测试
    print(f"打印请求失败信息的前1000个字符内容: {content.text[:1000]}...\n")
    # 保存错误信息文件至本地
    content.write_to_file(error_file_path)
    print(f"完整的请求失败信息已保存至本地错误文件error.jsonl\n")

def run_batch_job(input_file_path, output_file_path , error_file_path):
    # 文件路径

    batch_client = OpenAI(
    # 若没有配置环境变量,可用阿里云百炼API Key将下行替换为：api_key="sk-xxx",但不建议在生产环境中直接将API Key硬编码到代码中,以减少API Key泄露风险.
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下是北京地域base-url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"  # 阿里云百炼服务的base_url
)
    
    try:
        # Step 1: 上传包含请求信息的JSONL文件,得到输入文件ID,如果您需要输入OSS文件,可将下行替换为：input_file_id = "实际的OSS文件URL或资源标识符"
        input_file_id = upload_file(input_file_path)
        # Step 2: 基于输入文件ID,创建Batch任务
        batch_id = create_batch_job(input_file_id)
        # Step 3: 检查Batch任务状态直到结束
        status = ""
        while status not in ["completed", "failed", "expired", "cancelled"]:
            status = check_job_status(batch_id)
            print(f"等待任务完成...")
            time.sleep(10)  # 等待10秒后再次查询状态
        # 如果任务失败,则打印错误信息并退出
        if status == "failed":
            batch = qwen_client.batches.retrieve(batch_id)
            print(f"Batch任务失败。错误信息为:{batch.errors}\n")
            print(f"参见错误码文档: https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
            return
        # Step 4: 下载结果：如果输出文件ID不为空,则打印请求成功结果的前1000个字符内容，并下载完整的请求成功结果到本地输出文件;
        # 如果错误文件ID不为空,则打印请求失败信息的前1000个字符内容,并下载完整的请求失败信息到本地错误文件.
        output_file_id = get_output_id(batch_id)
        if output_file_id:
            download_results(output_file_id, output_file_path)
        error_file_id = get_error_id(batch_id)
        if error_file_id:
            download_errors(error_file_id, error_file_path)
            print(f"参见错误码文档: https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
    except Exception as e:
        print(f"An error occurred: {e}")
        print(f"参见错误码文档: https://help.aliyun.com/zh/model-studio/developer-reference/error-code")


def init_openai_client_with_qwen(dashscope_base_url= "https://dashscope.aliyuncs.com/compatible-mode/v1" 
                          ) -> OpenAI:
    dashscope_api_key = get_env("DASHSCOPE_API_KEY")
    
    # 初始化客户端
    qwen_client = OpenAI(
        # 若没有配置环境变量,可用阿里云百炼API Key将下行替换为：api_key="sk-xxx",但不建议在生产环境中直接将API Key硬编码到代码中,以减少API Key泄露风险.
        # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        api_key= dashscope_api_key,
        # 以下是北京地域base-url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
        base_url= dashscope_base_url # 阿里云百炼服务的base_url
    )
    return qwen_client


def call_qwen_with_openai_client(prompt:str="who are you?",
                                 response_format:BaseModel=None, 
                                 model_name= QWEN_PLUS,temperature= 0):
  """
  请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code
  # 我是通义千问，阿里巴巴集团旗下的超大规模语言模型。我能够回答问题、创作文字，如写故事、公文、邮件、剧本等，还能进行逻辑推理、编程，甚至表达观点和玩游戏。我支持多种语言，包括中文、英文、德语、法语、西班牙语等。如果你有任何问题或需要帮助，欢迎随时告诉我！
  # 我是通义千问（Qwen），阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我可以帮助你回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。如果你有任何问题或需要帮助，欢迎随时告诉我！
  """
  try:
      client = init_openai_client_with_qwen()
      response_content = call_openai_client(client=client, prompt=prompt,response_format=response_format,model_name=model_name,temperature=temperature)
      return response_content

  except Exception as e:
      print(f"error: {e}")
      raise e


def init_langchain_chat_tongyi( model_name="qwen-plus", temperature=0,top_p=0.8, max_tokens=2000):
    """https://docs.langchain.com/docs/integrations/llms/qwen
    """
    # Initialize the Qwen-Plus model
    chat_model = ChatTongyi(
        model_name= model_name,  # Specify Qwen-Plus model
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens
    )
    return chat_model

def init_langchain_chat_openai(model_name="qwen-plus", temperature=0,top_p=0.8, max_tokens=2000):
    """Initialize the OpenAI Chat model using LangChain's integration."""
    
    api_key = get_env("DASHSCOPE_API_KEY")
    
    chat_model = ChatOpenAI(
        model_name="qwen-plus",
        api_key=api_key,
        base_url=DASHSCOPE_BASE_URL,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens
    )
    return chat_model
  
  
def run_langchain_chat_model(use_chat_tongyi=False):
    """https://docs.langchain.com/oss/python/integrations/chat/tongyi
    """
    if use_chat_tongyi:
      # Initialize the Qwen-Plus model
      chat_model = init_langchain_chat_tongyi()
    else:
      chat_model = init_langchain_chat_openai()

    # Create messages
    messages = [
        SystemMessage(content="You are a helpful assistant."),
        HumanMessage(content="Hello, how are you?")
    ]

    # Get response
    response = chat_model.invoke(messages)
    print(response.content)

  
def run_qwen_model_chain():
    # Initialize the model
    llm = init_langchain_chat_tongyi()

    # Create a prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant that answers questions concisely."),
        ("user", "{question}")
    ])

    # Create a chain
    chain = prompt | llm | StrOutputParser()

    # Use the chain
    result = chain.invoke({"question": "What are the benefits of using Qwen-Plus?"})
    print(result)



if __name__ == "__main__":
  load_env()

  # response = call_qwen_with_openai_client()
  # print(response)
  
  run_langchain_chat_model(use_chat_tongyi=False)
  
  # run_qwen_model_chain()
