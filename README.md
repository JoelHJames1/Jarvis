# Artificial Intelligence Chat Bot

FrontEnd  React   
BackEnd  WebAPI  Flask running LLAMA.CPP


**AI Conversation Model Application**

This application uses a language model called Llama to generate conversational responses. Llama is wrapped into a Flask application and allows us to ask it questions and get AI-generated answers in response. The application also leverages Flask-CORS to handle Cross-Origin Resource Sharing (CORS), making cross-origin AJAX possible.

**Llama Model**
Llama is a generative language model used for answering questions. We've trained it on a specific conversation template, and it uses this template to generate its responses.

**Model Loading**
The language model files are stored in the ./Models directory. The application automatically selects the first model it finds in this directory for use in generating responses.

The model is loaded into an instance of LlamaCpp with some specific parameters, like the number of GPU layers, batch size, maximum tokens, and callbacks for handling output. This instance is then used in the LLMChain to connect prompts with the Llama model.

**Prompt Template**
A PromptTemplate is used to define the structure of the conversation. The application provides a template in which {question} will be replaced by the question provided by the user. This template is then used by the LLMChain to generate a complete prompt that includes the user's question.

**Flask Application**
The Flask application exposes a single POST endpoint at /ask. This endpoint accepts a JSON body with a 'question' field. When a request is sent to this endpoint, the Flask application uses the LLMChain to generate a response from the Llama model and then sends this response back to the client.

The question is inserted into the template to form a complete conversation prompt, which is then given to the Llama model. The model generates a response to the question based on the pattern it learned during training.

The generated response is then returned in the response body as JSON.

Running the Application
The application can be run directly from the command line with the command python app.py (or whatever you've named your main application file). The application will start and be accessible at http://localhost:5000, or another port if specified.

When the application is running, you can send a POST request to http://localhost:5000/ask with a JSON body that contains a 'question' field. The value of this field should be the question that you want to ask the model.

For example, you could use the following curl command to send a question:

bash
Copy code
curl -X POST -H "Content-Type: application/json" -d '{"question":"What is the meaning of life?"}' http://localhost:5000/ask
In response, you'll get a JSON object that contains the model's answer to your question.

Please note, the model was trained to simulate a conversational AI assistant "Jarvis" and will format responses accordingly. If you'd like to have a different format of response, you will need to adjust the PromptTemplate.

Requirements
To run this application, you need to have Flask, Flask-CORS, and the language model libraries installed. The model file also needs to be located in the specified ./Models directory.
