import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if __name__ == '__main__':
    prompt = PromptTemplate.from_template("{flower}의 꽃말을?")

    model = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            google_api_key=gemini_api_key
        )

    output_parser = StrOutputParser()

    chain = prompt | model | output_parser

    result = chain.invoke({"flower": "해바라기"})

    print(result)