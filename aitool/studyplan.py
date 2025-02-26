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
# Define the generation configuration for the study planner
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
}

# Create the model instance for the study planner
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-lite-preview-02-05",
    generation_config=generation_config,
)

def generate_study_plan(subjects_dates, extra_details=""):
    """
    Generates a detailed study plan schedule based on exam dates and subjects.

    Args:
        subjects_dates (dict): A dictionary where each key is a subject and the corresponding
                               value is the exam date (as a string, e.g., "2025-03-01").
        extra_details (str): Optional extra instructions such as preferred study hours or days off.

    Returns:
        str: A study plan schedule organized in a structured format.
    """
    # Format the subjects and exam dates into a human-readable list
    details = "\n".join([f"- {subject}: {date}" for subject, date in subjects_dates.items()])
    
    # Create the user prompt using a "Trip Ideas" style approach for structured planning
    prompt = (
        "Using a 'Trip Ideas' approach to scheduling, generate a detailed study plan for a student. "
        "Below are the subjects and their exam dates:\n\n"
        f"{details}\n\n"
        f"{extra_details}\n"
        "Please include a clear timeline that indicates when to study each subject, incorporate revision sessions, "
        "practice tests, and breaks, and present the study plan in a structured, table-like format."
    )
    
    # Set up the system message to instruct the model about its role
    # Define the user message to set the study planner context
    context_message = {
        "role": "user",
        "parts": [
            "You are an AI-powered study planner. Your task is to create a detailed, structured study schedule for a student "
            "based on their subjects and exam dates."
        ]
    }

    # Create the user message with the formatted prompt
    user_message = {
        "role": "user",
        "parts": [prompt]
    }

    # Start a chat session with the study planner context and send the prompt
    chat_session = model.start_chat(history=[context_message, user_message])

    response = chat_session.send_message("Generate the study plan based on the given exam dates and subjects.")
    return response.text

# Example usage of the study planner function
# if __name__ == "__main__":
#     # Define the subjects and exam dates
#     subjects_dates = {
#         "Mathematics": "2025-03-01",
#         "Physics": "2025-03-05",
#         "Chemistry": "2025-03-03",
#         "Biology": "2025-03-07",
#     }
    
#     # Optional extra instructions: preferred study times, days off, etc.
#     extra_details = "I prefer studying in the evenings and need at least one full day off per week for relaxation."
    
#     # Generate and print the study plan
#     study_plan = generate_study_plan(subjects_dates, extra_details)
#     print("Generated Study Plan:")
#     print(study_plan)
