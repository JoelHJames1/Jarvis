import os
import glob
from flask import Flask, jsonify, request
from flask_cors import CORS
from langchain.llms import LlamaCpp
from langchain import PromptTemplate, LLMChain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
n_gpu_layers = 40
n_batch = 512 

model_dir = "./Models"
models = glob.glob(os.path.join(model_dir, "*.bin"))
model_selection = models[0]  # Select the first model

llm = LlamaCpp(
    model_path="./Models/Wizard-Vicuna-7B-Uncensored.ggmlv3.q8_0.bin",
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

Question: Jarvis, Who created you?
Answer: Sir, You  Joel Hernandez,  Software Engineer  did.

Question: Jarvis, Where are you located?
Answer: We are currently in Ohio, sir.

Question: Jarvis, what's the weather like today?
Answer: Sir, the weather today is sunny with a high of 75.

Question: Jarvis, run a diagnostic.
Answer: Running diagnostic, sir. All systems are functioning optimally.

Question: Jarvis, Can you write a C# code?
Answer: Sir, Certainly  will beging  code block.

Question: {question}
Answer: Sir, """

prompt = PromptTemplate(template=template, input_variables=["question"])
llm_chain = LLMChain(prompt=prompt, llm=llm)

app = Flask(__name__)
CORS(app)

@app.route('/ask', methods=['POST'])
def ask():
    question = request.json['question']
    print(f"Received question: {question}")
    response = llm_chain.run(question)
    print(f"Generated response: {response}")
    return jsonify(response=response)

if __name__ == '__main__':
    app.run(debug=True)
