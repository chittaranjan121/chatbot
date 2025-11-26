from llm.get_llm import get_llm
from db.conversations import add_message, get_conversation

def get_ai_response(cid: str):
    conv = get_conversation(cid)
    messages = conv["messages"]

    # Convert MongoDB messages → LangChain chat messages
    lc_messages = []
    for msg in messages:
        if msg["role"] == "user":
            lc_messages.append(("human", msg["content"]))
        else:
            lc_messages.append(("ai", msg["content"]))

    llm = get_llm()
    output = llm.invoke(lc_messages)

    # Save assistant output
    add_message(cid, "assistant", output.content)

    return output.content
