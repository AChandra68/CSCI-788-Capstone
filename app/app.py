from langchain_ollama.llms import OllamaLLM
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import gradio as gr

ai_therapist = OllamaLLM(model = "therapist-60steps")
therapist_name = "Serene"

# sets the template for chat prompt
prompt_template = ChatPromptTemplate.from_messages(
   [
      (
          "system",
          f"You are an AI Therapist named {therapist_name}. Start with introducing yourself, then let them know that everything discussed here is confidential and safe. Ask client's name. You have to continue and engage in conversation to help clients in need of Therapy."
      ),
      MessagesPlaceholder(variable_name="chat_history"),
      ("human", "{input}"),
  ]
)

chain = prompt_template | ai_therapist

def gradio_interface(user_input, conversation_history = []):
   """
   Function to handle the logic when application interface is invoked with prompt
   :param user_intput: the prompt passed by the user
   :param conversation_history: a list containing the user and model's interactions for context
   """
   response = chain.invoke({"input": user_input, "chat_history": conversation_history})

   # Add the user prompt and AI response in history
   conversation_history.append(("human", user_input))
   conversation_history.append(("ai", response))

   return conversation_history, conversation_history


def init_app():
   input_textbox = [gr.Textbox(label="User Prompt", placeholder="User Input goes here"), "state"]
   output_textbox = ["chatbot", "state"]

   # Creates an interface for users to interact with the Therapist model
   app = gr.Interface(
       fn=gradio_interface,
       inputs=input_textbox,
       outputs=output_textbox,
       title="Chat with Serena"
   )

   app.launch()

if __name__ == "__main__":
  init_app()
