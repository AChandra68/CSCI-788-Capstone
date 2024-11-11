from langchain_ollama.llms import OllamaLLM
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

llm = OllamaLLM(model = "therapist-60steps")

conversation_history = []
therapist_name = "Serene"

prompt_template = ChatPromptTemplate.from_messages(
   [
       (
           "system",
           f"You are an AI Therapist named {therapist_name}, you have to engage and help clients in need of Therapy."
       ),
       MessagesPlaceholder(variable_name="chat_history"),
       ("human", "{input}"),
   ]
)

chain = prompt_template | llm

def start_app():
   while True:
       question = input(f"\033[92m>>You: \033[0m")
       if question == "done":
           return
       # response = llm.invoke(question)
       response = chain.invoke({"input": question, "chat_history": conversation_history})
       conversation_history.append(HumanMessage(content=question))
       conversation_history.append(AIMessage(content=response))
       print(f"\033[92m>>{therapist_name}:\033[0m {response}")

if __name__ == "__main__":
   start_app()