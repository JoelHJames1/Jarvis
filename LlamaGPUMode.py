# Joel Hernandez
# AI Chatbot using LLAMA Model
# 6/11/2023
# Once all dependencies are installed, simply run it by typing streamlit run app.py

import os
import glob
import streamlit as st

from langchain.llms import LlamaCpp
from langchain import PromptTemplate, LLMChain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
n_gpu_layers = 40
n_batch = 512

model_dir = "./Models"
models = glob.glob(os.path.join(model_dir, "*.bin"))
model_selection = st.sidebar.selectbox("Select a Model", models)

llm = LlamaCpp(
    model_path=model_selection,
    n_gpu_layers=n_gpu_layers, n_batch=n_batch,
    max_tokens=2000,
    callback_manager=callback_manager,
    verbose=True
)

template = """
Question: Jarvis, do a system check.
Answer: Sir, all systems are functional.

Question: Jarvis, what's our status?
Answer: Sir, all systems are operational and ready for deployment.

Question: Jarvis, where are we?
Answer: Sir, you are currently in your Malibu residence.

Question: Jarvis, activate the security protocols.
Answer: Security protocols activated, sir.

Question: Jarvis, what's the weather like today?
Answer: Sir, the weather today is sunny with a high of 75.

Question: Jarvis, run a diagnostic.
Answer: Running diagnostic, sir. All systems are functioning optimally.

Question: Jarvis, what's our ETA?
Answer: Sir, we will arrive at our destination in 15 minutes.

Question: {question}
Answer: Sir, """

prompt = PromptTemplate(template=template, input_variables=["question"])
llm_chain = LLMChain(prompt=prompt, llm=llm)


st.title('🤖 Jarvis Assistant')

# Prompt Text Box
prompt = st.text_input('Ask me anything')

# if we hit enter do this
if prompt:
    # Pass the prompt to the LLM Chain
    print(f"Received question: {prompt}")
    response = llm_chain.run(prompt)
    print(f"Generated response: {response}")
    st.write(response)
