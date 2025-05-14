from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from deepseek_llm import DeepSeekLLM
import os

load_dotenv()

# 初始化模型（注意使用pydantic v1的配置方式）
llm = DeepSeekLLM(
    api_key=os.getenv("DEEPSEEK_API_KEY"),  # 自动识别别名
    model="deepseek-chat",
    temperature=0.5
)

# 构建链
prompt_template = ChatPromptTemplate.from_template("{question}")
chain = prompt_template | llm | StrOutputParser()

# 执行
question = input("请输入问题：")
result = chain.invoke({"question": question})
print("回答：", result)