import streamlit as st
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()


## langsmith tracking
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_PROJECT"]="Q&A CHATBOT"
os.environ["LANGCHAIN_TRACKING_V2"]="true"


## prompt template

prompt=ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful assistant . Please respond to the user queries"),
        ("user","Question:{question}")
    ]
)

def generate_response(question,api_key,temperature,max_tokens):
    groq_api_key=api_key
    llm = ChatGroq(groq_api_key=groq_api_key, model_name="Llama3-8b-8192")
    outputparser=StrOutputParser()
    chain = prompt | llm | outputparser
    answer=chain.invoke({'question':question})
    return answer


## title of the app
st.title("Q&A Chatbot")
api_key=st.sidebar.text_input("Enter your Groq API key",type="password")

## temperature and tokens value
temperature= st.sidebar.slider("Temperature",min_value=0.0,max_value=1.0,value=0.7)
max_tokens= st.sidebar.slider("Max Tokens",min_value=50,max_value=300,value=150)

## main interface for user input
st.write("Question?")
user_input=st.text_input("You:")

if user_input:
    response=generate_response(user_input,api_key, temperature, max_tokens)
    st.write(response)
else:
    st.write("Please provide the input")



