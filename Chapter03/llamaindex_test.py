import os
from dotenv import load_dotenv

# [변경 1] 최신 Google GenAI 패키지에서 import
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding

from llama_index.core import VectorStoreIndex, Settings
from llama_index.core import SimpleDirectoryReader

load_dotenv()

Settings.llm = GoogleGenAI(
    model="gemini-2.5-flash-lite",
    api_key=os.getenv("GEMINI_API_KEY")
)

Settings.embed_model = GoogleGenAIEmbedding(
    model_name="text-embedding-004", # 최신 임베딩 모델 권장
    api_key=os.getenv("GEMINI_API_KEY")
)

if __name__ == '__main__':
    if not os.path.exists("data"):
        os.makedirs("data")
        with open("data/test.txt", "w", encoding="utf-8") as f:
            f.write("꽃말의 비밀 정원의 직원에게는 관리자, 정원사, 안내원 3가지 역할이 있습니다. 에이전트 이름은 '로즈'입니다.")

    documents = SimpleDirectoryReader("data").load_data()

    # 문서의 색인 생성
    index = VectorStoreIndex.from_documents(documents)

    # 요청 엔진 생성
    agent = index.as_query_engine()

    # 요청 예제
    response = agent.query("꽃말의 비밀 정원의 직원에게는 몇 가지 역할이 있나요?")
    print(f"Q: 꽃말의 비밀 정원의 직원들에게는 몇 가지 역할이 있나요?\nA: {response}\n")

    response = agent.query("꽃말의 비밀 정원의 에이전트 이름은 무엇인가요?")
    print(f"Q: 꽃말의 비밀 정원의 에이전트 이름은 무엇인가요?\nA: {response}\n")

    # 색인을 로컬에 저장
    index.storage_context.persist()