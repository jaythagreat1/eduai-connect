from langchain_core.prompts import PromptTemplate
from langchain_aws import ChatBedrock
import boto3

# Create a prompt template that rewrites a teacher question into a search

hyde_template = """Rewrite this teacher's question into a specific search query about student data.
Focus on specific metrics like grades, scores, attendance rate, engagement score, and course names.

Original question: {question}

Rewritten search query:"""

hyde_prompt = PromptTemplate(
    input_variables=["question"],
    template=hyde_template,
)

region = "us-east-1"
bedrock_runtime = boto3.client(service_name="bedrock-runtime", region_name=region)

llm = ChatBedrock(
    client=bedrock_runtime,
    model_id="anthropic.claude-3-sonnet-20240229-v1:0",
    model_kwargs={"temperature": 0, "max_tokens": 1000},
)


# Generate a search query from the original question
def transform_query(question: str) -> str:
    prompt = hyde_prompt.format(question=question)
    response = llm.invoke(prompt)
    # return text/content depending on the SDK response shape
    return getattr(response, "content", str(response))


if __name__ == "__main__":
    result = transform_query("who needs help")
    print(result) 