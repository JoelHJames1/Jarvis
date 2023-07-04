# Required imports
import os
import streamlit as st
import torch
import transformers
from torch import cuda, bfloat16
from transformers import StoppingCriteria, StoppingCriteriaList

# Checking if CUDA is available
device = f'cuda:{cuda.current_device()}' if cuda.is_available() else 'cpu'

# Print if CUDA is available or not
if cuda.is_available():
    print("CUDA is available. PyTorch is using GPU.")
    print("Device ID:", device)
    print("Device Name:", torch.cuda.get_device_name(device))
else:
    print("CUDA is not available. PyTorch is using CPU.")

# Model Loading
model = transformers.AutoModelForCausalLM.from_pretrained(
    'ehartford/Wizard-Vicuna-13B-Uncensored',  # replace with path to your model directory 'mosaicml/mpt-7b-instruct'
    trust_remote_code=True,
    torch_dtype=bfloat16,
    max_seq_len=2048
)



# Move the model to GPU device
model.to(device)

# Tokenizer
tokenizer = transformers.AutoTokenizer.from_pretrained("EleutherAI/gpt-neox-20b")

# Stopping Criteria
stop_token_ids = tokenizer.convert_tokens_to_ids([""])

class StopOnTokens(StoppingCriteria):
    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
        for stop_id in stop_token_ids:
            if input_ids[0][-1] == stop_id:
                return True
        return False

stopping_criteria = StoppingCriteriaList([StopOnTokens()])

# HF Pipeline
generate_text = transformers.pipeline(
    model=model, tokenizer=tokenizer,
    return_full_text=True,
    task='text-generation',
    device=device,
    stopping_criteria=stopping_criteria,
    temperature=0.1,
    top_p=0.15,
    top_k=0,
    max_new_tokens=64,
    repetition_penalty=1.1
)

# Streamlit
st.title('🤖 Jarvis Assistant')

# Define a conversation history
conversation_history = [
    "Question: Jarvis, do a system check.\nAnswer: Sir, all systems are functional.\n",
    "Question: Jarvis, what's our status?\nAnswer: Sir, all systems are operational and ready for deployment.\n",
    "Question: Jarvis, where are we?\nAnswer: Sir, you are currently in your Malibu residence.\n",
    "Question: Jarvis, activate the security protocols.\nAnswer: Security protocols activated, sir.\n",
    "Question: Jarvis, what's the weather like today?\nAnswer: Sir, the weather today is sunny with a high of 75.\n",
    "Question: Jarvis, run a diagnostic.\nAnswer: Running diagnostic, sir. All systems are functioning optimally.\n",
    "Question: Jarvis, what's our ETA?\nAnswer: Sir, we will arrive at our destination in 15 minutes.\n",
]

# Prompt Text Box
prompt = st.text_input('Ask me anything')

# if we hit enter do this
if prompt:
    # Add the new question to the conversation history
    conversation_history.append(f"Question: Jarvis, {prompt}\nAnswer: ")

    # Pass the conversation history to the generate_text pipeline
    response = generate_text("".join(conversation_history))

    # Extract the model's response
    model_response = response[0]['generated_text'].split("Answer: ")[-1]

    # Add the model's response to the conversation history
    conversation_history.append(f"{model_response}\n")

    # Print the model's response
    st.write(model_response)
