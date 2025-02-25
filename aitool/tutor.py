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

# Define the generation configuration for the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
}

# Create the model instance
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-lite-preview-02-05",
    generation_config=generation_config,
)

# Start a chat session with a system prompt that sets the tutor's context
initial_history = [
    {
        "role": "system",
        "parts": [
            "You are a helpful math tutor and worksheet generator. "
            "You can solve any type of math problem with detailed, step-by-step explanations "
            "and generate custom worksheets with practice problems on any given math topic."
        ],
    }
]

chat_session = model.start_chat(history=initial_history)

def solve_math_problem(problem):
    """
    Solves a given math problem and returns a detailed step-by-step explanation.
    
    Args:
        problem (str): A math problem in string format.
    
    Returns:
        str: Detailed explanation and solution to the math problem.
    """
    prompt = f"Solve the following math problem and provide a detailed, step-by-step explanation:\n\n{problem}"
    response = chat_session.send_message(prompt)
    return response.text

def generate_worksheet(topic, num_questions=5):
    """
    Generates a worksheet on a specified math topic with a given number of problems.
    Each problem is accompanied by a detailed explanation after a designated break.
    
    Args:
        topic (str): The math topic (e.g., 'quadratic equations', 'linear functions').
        num_questions (int): The number of problems to include in the worksheet.
    
    Returns:
        str: The generated worksheet with problems and detailed solutions.
    """
    prompt = (
        f"Generate a worksheet on the topic '{topic}' containing {num_questions} problems. "
        "List the problems first without giving away the solutions. After listing the problems, "
        "provide a detailed, step-by-step solution for each problem."
    )
    response = chat_session.send_message(prompt)
    return response.text

# Example usage of the functions
if __name__ == "__main__":
    # Example 1: Solve a generic math problem
    math_problem = "Solve for x: 2x + 5 = 17"
    solution = solve_math_problem(math_problem)
    print("Solution for the math problem:")
    print(solution)
    
    # Example 2: Generate a worksheet on quadratic equations
    worksheet = generate_worksheet("quadratic equations", num_questions=5)
    print("\nGenerated Worksheet on Quadratic Equations:")
    print(worksheet)
