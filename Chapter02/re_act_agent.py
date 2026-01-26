import os

from dotenv import load_dotenv
from langchain_classic import hub
from langchain_classic.agents import create_react_agent, AgentExecutor
from langchain_community.utilities import SerpAPIWrapper
from langchain_core.tools import Tool
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

open_ai_api_key = os.getenv("OPEN_AI_API_KEY")
serp_api_key = os.getenv("SERP_API_KEY")
lang_smith_api_key = os.getenv("LANG_SMITH_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")

if __name__ == '__main__':

    prompt = hub.pull("hwchase17/react", api_key=lang_smith_api_key)

    print(prompt)

    # 책에는 open ai로 되어있으나 gemini는 api 프리티어 제공이 있어 gemini로 base llm 변경
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        google_api_key=gemini_api_key
    )


    search = SerpAPIWrapper(serpapi_api_key=serp_api_key)

    tools = [
        Tool(
            name="Search",
            func=search.run,
            description="LLM이 관련 지식이 없을 때 지식 검색에 사용됩니다."
        ),
    ]

    # ReAct 에이전트 생성
    agent = create_react_agent(llm, tools, prompt)

    # 에이전트와 도구를 전달하여 AgentExecutor생성
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    print("첫 번째 실행 결과 :")
    agent_executor.invoke({"input" : "현재 인공지능 에이전트의 최신 연구 동향은 무엇입니까?"})
    print("두 번째 실행 결과:")
    agent_executor.invoke({"input":"현재 인공지능 에이전트의 최신 연구 동향은 무엇입니까?"})
