from fastapi import FastAPI
from langserve import add_routes
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

load_dotenv()

app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="Simple translation API with LangServe"
)

# Prompt template:
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a translation engine. Always translate the user's message into the target {language}. Output ONLY the translated text. No greetings, no explanations."),
    ("user", "{text}")
])

model = ChatOpenAI(model="gpt-4o-mini")

parser = StrOutputParser()

chain = prompt | model | parser

# Expose chain as API
add_routes(
    app,
    chain,
    path="/chain",
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
