import os
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai import GenerativeModel

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

model = GenerativeModel(
# model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-lite-preview-02-05",
    generation_config=generation_config,
)

# Start a chat session with a system prompt that sets the tutor's context
chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "You are a math tutor who can teach and help solve all types of math problems, from basic to advanced levels and you can provide me all types of questions and worksheets on my demand. Teach me a lesson on quadratic equations. Assume I know absolutely nothing about it."
      ],
    },
    {
      "role": "model",
      "parts": [
        "## Quadratic Equations: A Beginner's Guide\n\nImagine you're throwing a ball up in the air. It goes up, reaches a peak, and then falls back down. The path it takes can be described by a **quadratic equation**. Let's explore what that means:\n\n**1. What is a Quadratic Equation?**\n\nIt's an equation that looks like this: **ax² + bx + c = 0**. Don't be intimidated by the symbols! Let's break it down:\n\n* **x**: This represents an unknown value, like the time it takes for the ball to reach the ground.\n* **a, b, c**: These are numbers, like the initial speed of the ball, its starting height, and the effect of gravity.\n* **²**: This means 'squared,' or multiplied by itself. For example, x² is the same as x times x.\n\n**2. Why are they called 'Quadratic'?**\n\nThe word 'quadratic' comes from 'quad,' which means 'square.' The highest power of x in the equation is 2, hence the name.\n\n**3. What do they tell us?**\n\nQuadratic equations help us solve problems where things change in a non-linear way, like the ball's trajectory. Solving the equation means finding the values of x that make the equation true. These values are called **roots** or **solutions**.\n\n**4. How do we solve them?**\n\nThere are different ways to solve quadratic equations:\n\n* **Factoring**: This involves rewriting the equation as a product of two simpler expressions.\n* **Quadratic Formula**: This is a powerful formula that can solve any quadratic equation. It looks scary, but it's just a recipe for finding the roots.\n* **Graphing**: You can plot the equation on a graph and see where it crosses the x-axis. Those points are the solutions.\n\n**5. Why are they important?**\n\nQuadratic equations have applications in various fields:\n\n* **Physics**: Calculating the motion of objects, like our ball example.\n* **Engineering**: Designing bridges, buildings, and other structures.\n* **Finance**: Predicting market trends and making investment decisions.\n* **Computer Science**: Used in algorithms and computer graphics.\n\n**6. Let's see an example:**\n\nImagine the equation describing the ball's height is: **h = -5t² + 20t + 10**. Here, h is the height and t is the time. Solving this equation will tell us when the ball hits the ground (h = 0). We can use the quadratic formula or graph the equation to find the solutions.\n\nThis is just a basic introduction to quadratic equations. There's much more to learn, but hopefully, this gives you a starting point to explore further!"
      ],
    },
    {
      "role": "user",
      "parts": [
        "Give me an equation to solve and test my knowledge. Don't give answers just yet."
      ],
    },
    {
      "role": "model",
      "parts": [
        "**Solve the following quadratic equation:**\n\n**x² - 5x + 6 = 0**\n\nRemember, the solutions are the values of x that make the equation true. You can use any method you like, such as factoring, the quadratic formula, or graphing. Good luck! "
      ],
    },
    {
      "role": "user",
      "parts": [
        "x=0 and x=10"
      ],
    },
    {
      "role": "model",
      "parts": [
        "Unfortunately, x = 0 and x = 10 are not solutions to the equation x² - 5x + 6 = 0. \n\nLet's check:\n\n* For x = 0: (0)² - 5(0) + 6 = 6 ≠ 0\n* For x = 10: (10)² - 5(10) + 6 = 56 ≠ 0\n\nAs you can see, neither value makes the equation true. \n\nTry using another method like factoring or the quadratic formula to find the correct solutions. "
      ],
    },
    {
      "role": "user",
      "parts": [
        "Provide a detailed method to solve it."
      ],
    },
    {
      "role": "model",
      "parts": [
        "## Solving x² - 5x + 6 = 0: A Step-by-Step Guide\n\nLet's solve this equation using two different methods: factoring and the quadratic formula.\n\n**Method 1: Factoring**\n\n1. **Identify the factors of the constant term (c) whose sum is the coefficient of the linear term (b).** \n    * In this case, c = 6 and b = -5. \n    * We need to find two numbers that multiply to 6 and add up to -5. These numbers are -2 and -3.\n\n2. **Rewrite the middle term using the identified factors.**\n    * x² - 5x + 6 becomes x² - 2x - 3x + 6.\n\n3. **Group the terms and factor by grouping.**\n    * (x² - 2x) + (-3x + 6)\n    * x(x - 2) - 3(x - 2)\n\n4. **Factor out the common binomial.**\n    * (x - 2)(x - 3)\n\n5. **Set each factor equal to zero and solve for x.**\n    * x - 2 = 0 → x = 2\n    * x - 3 = 0 → x = 3\n\nTherefore, the solutions to the equation are **x = 2 and x = 3**.\n\n**Method 2: Quadratic Formula**\n\nUsing **x = (-b ± √(b² - 4ac)) / (2a)**, we substitute a = 1, b = -5, and c = 6, leading to the same solutions: **x = 2 and x = 3**.\n\nBoth methods confirm the correct answers." 
      ],
    },
  ]
)


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
# if __name__ == "__main__":
#     # Example 1: Solve a generic math problem
#     math_problem = "Solve for x: 2x + 5 = 17"
#     solution = solve_math_problem(math_problem)
#     print("Solution for the math problem:")
#     print(solution)
    
#     # Example 2: Generate a worksheet on quadratic equations
#     worksheet = generate_worksheet("quadratic equations", num_questions=5)
#     print("\nGenerated Worksheet on Quadratic Equations:")
#     print(worksheet)
