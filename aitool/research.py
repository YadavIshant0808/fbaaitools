import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from the .env file
load_dotenv()

# Retrieve the API key from environment variables
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set in the .env file.")

# Configure the Gemini API using the loaded API key
genai.configure(api_key=gemini_api_key)

def fba_researcher(inp_message):
    # Create the model configuration
    generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
    }

    model = genai.GenerativeModel(
    model_name="gemini-2.0-pro-exp-02-05",
    generation_config=generation_config,
    )

    chat_session = model.start_chat(
    history=[
        {
        "role": "system",
        "parts": [
            "You are an expert scientific researcher with years of experience in conducting systematic literature surveys and meta-analyses. You pride yourself on incredible accuracy and attention to detail, always sticking to the facts provided and never fabricating new details."
        ]
        },
        {
        "role": "user",
        "parts": [
            "Now look at the research paper below, and answer the following questions in 1-2 sentences:\n"
            "1. When was the paper published?\n"
            "2. What is the sample size?\n"
            "3. What is the study methodology? In particular, is it a randomized control trial?\n"
            "4. How was the study funded? In particular, was the funding from commercial funders?\n"
            "5. What was the key question being studied?\n"
            "6. What were the key findings to the key question being studied?\n\n"
            "Research paper: "
        ]
        },
    ]
    )

    response = chat_session.send_message(inp_message)

    return(response.text)
