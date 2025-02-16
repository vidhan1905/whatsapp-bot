import os
import requests
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain

# Load your Groq API key from environment variables
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Initialize the Groq LLM for LangChain
groq_llm = ChatGroq(api_key=GROQ_API_KEY, model_name="llama-3.3-70b-versatile")

# Create a prompt template for LangChain
prompt_template = PromptTemplate(
    input_variables=["user_input"],
    template="You are a helpful assistant. Respond to: {user_input}"
)

# Create the LLM chain using LangChain
chain = LLMChain(llm=groq_llm, prompt=prompt_template)

# Set up the Flask app
app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    # Extract the incoming message from the POST request sent by Twilio
    incoming_msg = request.values.get('Body', '')
    print("Received message:", incoming_msg)  # for debugging

    # Use LangChain (and our Groq model) to generate a response
    ai_response = chain.run(user_input=incoming_msg)
    
    # Create a Twilio MessagingResponse and send the generated reply
    resp = MessagingResponse()
    resp.message(ai_response)
    return str(resp)

if __name__ == "__main__":
    # For local testing; PythonAnywhere will use its WSGI server configuration.
    app.run(host="0.0.0.0", port=8080, debug=True)
