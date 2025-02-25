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

# Set the common generation configuration for both tasks
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 65536,
    "response_mime_type": "text/plain",
}

# Create the model instance (using code execution tools if needed)
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-thinking-exp-01-21",
    generation_config=generation_config,
    tools='code_execution',  # This enables code execution when required
)

def optimize_code(code_snippet):
    """
    Analyzes and optimizes a given Python function.
    
    It identifies the time complexity, optimizes the code (e.g. replacing bubble sort
    with a more efficient algorithm), and explains why the new version is faster.
    
    Args:
        code_snippet (str): A Python function as a string.
    
    Returns:
        str: The optimized code along with a detailed explanation.
    """
    # Set up a system message for the code optimizer role.
    system_message = {
        "role": "system",
        "parts": [
            "You are a helpful code optimizer. Analyze the provided Python function, "
            "identify its time complexity, and optimize it. Provide a detailed explanation of "
            "the improvements made. Avoid using Python's in-built sort() method if sorting is involved."
        ]
    }
    
    # Create a user message including the code snippet.
    user_message = {
        "role": "user",
        "parts": [
            f"Here is a Python function:\n\n{code_snippet}\n\n"
            "Identify the time complexity, optimize the function, and explain why the optimized version is faster."
        ]
    }
    
    # Start a new chat session for code optimization.
    chat_session = model.start_chat(history=[system_message, user_message])
    
    # Send a prompt to trigger the optimization response.
    response = chat_session.send_message("Please provide the optimized code along with a detailed explanation.")
    return response.text

def generate_unit_tests(code_snippet):
    """
    Generates 10 unit tests for a given Python function along with comments and an explanation.
    
    Args:
        code_snippet (str): A Python function as a string.
    
    Returns:
        str: The unit tests and a short explanation of the testing strategy.
    """
    # Set up a system message for the unit testing role.
    system_message = {
        "role": "system",
        "parts": [
            "You are a helpful unit test generator. Your task is to create 10 distinct unit tests for "
            "the given Python function. Each test should include comments explaining its purpose. After listing "
            "the tests, provide a short explanation of the testing strategy used."
        ]
    }
    
    # Create a user message with the code snippet.
    user_message = {
        "role": "user",
        "parts": [
            f"Here is a Python function:\n\n{code_snippet}\n\n"
            "Please add 10 different unit tests for this function with comments, then follow up with a short explanation of what was done."
        ]
    }
    
    # Start a new chat session for generating unit tests.
    chat_session = model.start_chat(history=[system_message, user_message])
    
    # Send a prompt to trigger the unit tests response.
    response = chat_session.send_message("Please provide the unit tests along with the explanation.")
    return response.text

# Example usage of the functions
# if __name__ == "__main__":
#     # Example 1: Code Optimizer (Bubble sort example)
#     bubble_sort_code = """def sort_list(list_to_sort):
#     \"\"\" 
#     This function sorts a list of numbers in ascending order using the bubble sort algorithm.
    
#     Args:
#         list_to_sort: A list of numbers to be sorted.
    
#     Returns:
#         A new list with the numbers sorted in ascending order.
#     \"\"\"
#     # Create a copy of the list to avoid modifying the original
#     sorted_list = list_to_sort.copy()
#     n = len(sorted_list)
    
#     # Iterate through the list n-1 times
#     for i in range(n-1):
#         # Flag to track if any swaps were made in a pass
#         swapped = False
#         # Iterate through the unsorted portion of the list
#         for j in range(n-i-1):
#             # Compare adjacent elements and swap if necessary
#             if sorted_list[j] > sorted_list[j+1]:
#                 sorted_list[j], sorted_list[j+1] = sorted_list[j+1], sorted_list[j]
#                 swapped = True
#         # If no swaps were made, the list is already sorted
#         if not swapped:
#             break
    
#     # Return the sorted list
#     return sorted_list

# # Example usage:
# my_list = [1, 9, 5, 2, 1, 8, 6, 6, 3, 4, 10, 7]
# print(sort_list(my_list))  # Expected Output: [1, 1, 2, 3, 4, 5, 6, 6, 7, 8, 9, 10]"""

#     optimized_result = optimize_code(bubble_sort_code)
#     print("Optimized Code and Explanation:")
#     print(optimized_result)
    
#     # Example 2: Unit Testing Generator (Palindrome checker example)
#     palindrome_code = """def is_palindrome(word):
#     \"\"\" 
#     Checks whether a word is a palindrome.
    
#     Args:
#         word: The word to check.
    
#     Returns:
#         True if the word is a palindrome, False otherwise.
#     \"\"\"
    
#     # Convert the word to lowercase and remove non-alphanumeric characters.
#     word = ''.join(char.lower() for char in word if char.isalnum())
    
#     # Check if the word is the same forwards and backwards.
#     return word == word[::-1]"""

#     unit_tests_result = generate_unit_tests(palindrome_code)
#     print("\nGenerated Unit Tests and Explanation:")
#     print(unit_tests_result)
