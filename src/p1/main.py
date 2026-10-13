from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage,HumanMessage,AIMessage,ToolMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from tools import search_code,search_logs,run_tests
import warnings

warnings.filterwarnings('ignore')

load_dotenv()




def fromat_doc(docs):
    return "\n\n".join(doc.page_content for doc in docs)




model=ChatGroq(
    model="qwen/qwen3.8-27b",
    groq_api_key=os.getenv("API_KEY"),
    max_tokens=800
)
bug_report = """
Login API returns HTTP 500 when the password field is empty.

Expected:
HTTP 400 Bad Request.

Actual:
HTTP 500 Internal Server Error.

Endpoint:
POST /login
"""

promptTemplate=ChatPromptTemplate.from_messages(
    [
    (
        "system",
        """You are a senior software engineer investigating a bug.

Analyze the bug using the provided source-code evidence.

Important rules:
- Do not claim a root cause is confirmed unless the evidence supports it.
- Clearly separate evidence from assumptions.
- If the evidence is insufficient, say what additional evidence is needed.

"""
    ),
    (
        "human",
        """Bug Report:
Investigate this bug:

{bug_report}

You MUST investigate this bug using the available tools before
providing your final answer.

First use search_code to inspect the relevant implementation.
Use search_logs when log evidence is needed.

Do not provide a final answer based only on the bug report.
"""
    )
    ]
)
tools=[search_code,search_logs,run_tests]
model_with_tools=model.bind_tools(tools,tool_choice="auto")

chain = (
    {
        "bug_report":RunnablePassthrough()
    } | promptTemplate | model_with_tools
)
toop_mpa={
    tool.name:tool
    for tool in tools
}
res=chain.invoke(bug_report)
messages=[SystemMessage(content="""ou are a senior software engineer investigating a bug.

Analyze the bug using the provided source-code evidence.

Important rules:
- Do not claim a root cause is confirmed unless the evidence supports it.
- Clearly separate evidence from assumptions.
- If the evidence is insufficient, say what additional evidence is needed.""")]
messages.append(HumanMessage(content=bug_report))
messages.append(res)
while True:

    if not res.tool_calls:
        print(res.content)
        break

    for tc in res.tool_calls:
        tool=tc["name"]
        args=tc["args"]
        if tool not in toop_mpa:
            raise ValueError(f"Unknown tool: {tool}")
        res=toop_mpa[tool].invoke(args)
        messages.append(ToolMessage(content=res,tool_call_id=tc["id"]))

    res=model_with_tools.invoke(messages)
    messages.append(res)
        

    
            

    
