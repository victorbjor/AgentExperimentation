from openai import OpenAI
from pydantic import BaseModel, Field
import instructor
from textwrap import dedent
import ollama

client = instructor.from_openai(
    OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama",  # required, but unused
    ),
    mode=instructor.Mode.JSON,
)


class CriticalResponse(BaseModel):
    criticism: str = Field(
        description="Area of improvement in the answer from the agent",
    )
    new_answer: str = Field(
        description="New improved answer to the user",
    )

def generate_initial_response(query: str) -> str:
    return ollama.chat(
        messages=[
            {
                "role": "user",
                "content": query,
            }
        ],
        model="llama3.2",
    )['message']['content']

def query_step(query: str, last_answer: str) -> CriticalResponse:
    return client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": dedent(
                    f"""
                <UserQuery>
                {query}
                </UserQuery>
                
                <AgentAnswer>
                {last_answer}
                </AgentAnswer>

                Critical Response: An agent gave the above answer to a user query.
                Recall an item of criticism regarding the agent answer. 
                Then, provide a new rewritten response to the user based on this criticism.
                If you have absolutely no idea how to improve the answer, answer with an empty string.
                """
                ),
            }
        ],
        model="llama3.2",
        response_model=CriticalResponse,
    )


if __name__ == "__main__":
    query = (
        "Is there life on Mars?"
    )
    initial_answer = generate_initial_response(query)
    last_answer = initial_answer

    for i in range(50):
        print(f"Query: {query} - iteration {i+1}")
        response = query_step(query, last_answer)
        if (len(response.new_answer) < 3):
            break
        last_answer = response.new_answer
        print(f"\t\tCriticism: {response.criticism}")

    print("-------------------\n\n\n")
    print(f"Initial answer:\n\t{initial_answer}")
    print(f"Last answer:\n\t{last_answer}")

