import boto3
from langchain_aws import ChatBedrock, BedrockEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# -------------------------
# 1. AWS / Bedrock Setup
# -------------------------
region = "us-east-1"

bedrock_runtime = boto3.client(
    service_name="bedrock-runtime",
    region_name=region
)

# Claude model for generating answers
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

# Turn the vector store into a retriever — this searches for relevant docs
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# -------------------------
# 4. Prompt Template
# -------------------------
prompt = ChatPromptTemplate.from_template("""
You are an education analytics assistant that helps teachers understand student performance data.
Use the context below to answer the question. If the answer is not in the context, say you don't know.

Context:
{context}

Question:
{question}

Answer:
""")

# -------------------------
# 5. LCEL Chain — this is the modern LangChain way
# The | operator pipes data from one step to the next
# Step 1: Pass the question to retriever AND pass it through as-is
# Step 2: Format into the prompt template
# Step 3: Send to Claude on Bedrock
# Step 4: Parse the output as a string
# -------------------------
chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# -------------------------
# 6. Ask Questions
# -------------------------
if __name__ == "__main__":
    while True:
        q = input("\nAsk a question (or 'exit'): ")
        if q.lower() == "exit":
            break
        # chain.invoke() runs the full pipeline:
        # question → retriever finds docs → prompt formats it → Claude answers
        answer = chain.invoke(q)
        print("\nAnswer:", answer)