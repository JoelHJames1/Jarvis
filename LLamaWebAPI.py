# Joel Hernandez
# AI Chatbot using LLAMA Model
# 6/11/2023

import glob
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from langchain.llms import LlamaCpp
from langchain import PromptTemplate, LLMChain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
n_gpu_layers = 10
n_batch = 2

model_dir = "./Models"
models = glob.glob(os.path.join(model_dir, "*.bin"))
model_selection = models[0]

llm = LlamaCpp(
    model_path="./Models/airoboros-7b-gpt4.ggmlv3.q8_0.bin",
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



app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

@app.route('/ask', methods=['POST'])
def ask():
    prompt = request.json['question']  # Add this line to extract the question from the request
    print(f"Received question: {prompt}")
    response = llm_chain.run(prompt)
    print(f"Generated response: {response}")
    return jsonify(response=response)

if __name__ == '__main__':
    app.run(debug=True)
