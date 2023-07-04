import streamlit as st 
from langchain.agents.agent_toolkits import create_python_agent
from langchain.tools.python.tool import PythonREPLTool
from langchain import PromptTemplate, LLMChain
#from langchain.llms import GPT4All
import gpt4all


PATH = './Models'
llm = gpt4all.GPT4All(model_path=PATH, model_name="Wizard-Vicuna-30B-Uncensored.ggmlv3.q5_0")


agent_executor = create_python_agent(
    llm=llm,
    tool=PythonREPLTool(),
    verbose=True
)

st.title('🦜🔗 GPT For Y\'all')

prompt = st.text_input('Enter your prompt here!')

if prompt: 
    response = agent_executor.run(prompt)
    st.write(response)
