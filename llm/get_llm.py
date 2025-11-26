from langchain_openai import ChatOpenAI
import config.settings as settings

def get_llm():
    return ChatOpenAI(
        model=settings.OPENAI_MODEL,
        temperature=0.3,
        api_key=settings.OPENAI_API_KEY
    )
