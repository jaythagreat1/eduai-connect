import boto3
from langchain_aws import ChatBedrock, BedrockEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# -------------------------
# 1. AWS / Bedrock Setup
# -------------------------
region = "us-east-1"

bedrock_runtime = boto3.client(
    service_name="bedrock-runtime",
    region_name=region
)

llm = ChatBedrock(
    client=bedrock_runtime,
    model_id="anthropic.claude-3-sonnet-20240229-v1:0",
    model_kwargs={"temperature": 0, "max_tokens": 1000}
)

# -------------------------
# 2. Embeddings (must match vector_store.py)
# -------------------------
embeddings = BedrockEmbeddings(
    client=bedrock_runtime,
    model_id="amazon.titan-embed-text-v1"
)

# -------------------------
# 3. Load Saved FAISS Index
# -------------------------
vectorstore = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# -------------------------
# 4. Prompt Template (now includes chat_history)
# -------------------------
prompt = ChatPromptTemplate.from_template("""
You are an education analytics assistant that helps teachers understand student performance data.
Use the context below to answer the question. If the answer is not in the context, say you don't know.
Use the chat history to understand follow-up questions — if the user says "her" or "their", refer to the previous conversation.

Chat History:
{chat_history}

Context:
{context}

Question:
{question}

Answer:
""")

# -------------------------
# 5. Chain (retriever called separately so memory works)
# -------------------------
chain = (
    prompt
    | llm
    | StrOutputParser()
)

# -------------------------
# 6. Ask Questions with Memory
# -------------------------
if __name__ == "__main__":
    chat_history = ""
    while True:
        q = input("\nAsk a question (or 'exit'): ")
        if q.lower() == "exit":
            break
        docs = retriever.invoke(q)
        context = "\n\n".join([doc.page_content for doc in docs])
        answer = chain.invoke({
            "context": context,
            "question": q,
            "chat_history": chat_history
        })
        print("\nAnswer:", answer)
        chat_history += f"Human: {q}\nAssistant: {answer}\n"
