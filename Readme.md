Below is the complete Markdown content in an easily copiable format:

```markdown
# FBA Dev Tools Integration Guide

This guide is intended for our backend developers (Dev1  and Dev2) to help integrate AI tool functions into our Django project. We are not using APIs for these tools—instead, we will import the functions directly from our AI tool files, pass the required inputs, and then forward the output to the frontend for proper rendering.

## Project Structure Overview

- **optimise.py**
  - `optimize_code(code_snippet: str) -> str`  
    *Analyzes and optimizes a given Python function.*
  - `generate_unit_tests(code_snippet: str) -> str`  
    *Generates unit tests for the provided code snippet.*

- **research.py**
  - `fba_researcher(inp_message: str) -> str`  
    *Processes a research paper message and returns answers to specific research questions.*

- **studyplan.py**
  - `generate_study_plan(subjects_dates: dict, extra_details: str = "") -> str`  
    *Generates a detailed study plan schedule based on provided subjects and exam dates.*

- **tutor.py**
  - `solve_math_problem(problem: str) -> str`  
    *Provides a detailed, step-by-step solution for a given math problem.*
  - `generate_worksheet(topic: str, num_questions: int = 5) -> str`  
    *Generates a worksheet with math problems and detailed solutions.*

## How to Integrate

### 1. Importing the Functions

In your Django view file (e.g., `views.py`), import the functions as needed:

```python
from .optimise import optimize_code, generate_unit_tests
from .research import fba_researcher
from .studyplan import generate_study_plan
from .tutor import solve_math_problem, generate_worksheet
```

### 2. Creating View Functions

Below are sample view functions to demonstrate how to wrap these AI tool functions. Each view reads inputs from a POST request, calls the corresponding function, and then passes the output to a template.

#### **Code Optimiser Example**

This view calls `optimize_code` with a provided code snippet:

```python
def code_optimiser_view(request):
    if request.method == 'POST':
        code_snippet = request.POST.get('code_snippet', '')
        if code_snippet:
            result = optimize_code(code_snippet)
            return render(request, 'tool_output.html', {'result': result})
        else:
            return render(request, 'tool_output.html', {'error': 'Code snippet is missing.'})
    return render(request, 'code_optimiser.html')
```

#### **Study Planner Example**

This view calls `generate_study_plan`. It expects a JSON string for the subjects and dates and an optional extra details field:

```python
import json

def study_planner_view(request):
    if request.method == 'POST':
        subjects_dates_json = request.POST.get('subjects_dates', '')
        extra_details = request.POST.get('extra_details', '')
        try:
            subjects_dates = json.loads(subjects_dates_json)
        except json.JSONDecodeError:
            return render(request, 'tool_output.html', {'error': 'Invalid JSON for subjects and dates.'})
        result = generate_study_plan(subjects_dates, extra_details)
        return render(request, 'tool_output.html', {'result': result})
    return render(request, 'study_planner.html')
```

#### **Researcher Example**

This view calls `fba_researcher` with an input message:

```python
def researcher_view(request):
    if request.method == 'POST':
        inp_message = request.POST.get('inp_message', '')
        if inp_message:
            result = fba_researcher(inp_message)
            return render(request, 'tool_output.html', {'result': result})
        else:
            return render(request, 'tool_output.html', {'error': 'Input message is required.'})
    return render(request, 'researcher.html')
```

#### **Tutor Example**

This view handles two tutor actions: solving a math problem and generating a worksheet.

```python
def tutor_view(request):
    if request.method == 'POST':
        action = request.POST.get('action', '')
        if action == 'solve':
            problem = request.POST.get('problem', '')
            if problem:
                result = solve_math_problem(problem)
                return render(request, 'tool_output.html', {'result': result})
            else:
                return render(request, 'tool_output.html', {'error': 'Math problem is missing.'})
        elif action == 'worksheet':
            topic = request.POST.get('topic', '')
            try:
                num_questions = int(request.POST.get('num_questions', '5'))
            except ValueError:
                num_questions = 5
            if topic:
                result = generate_worksheet(topic, num_questions)
                return render(request, 'tool_output.html', {'result': result})
            else:
                return render(request, 'tool_output.html', {'error': 'Topic is missing.'})
    return render(request, 'tutor.html')
```

### 3. Frontend Integration

- **Templates:**  
  Create individual input templates (e.g., `code_optimiser.html`, `study_planner.html`, `researcher.html`, and `tutor.html`) where users can enter the necessary data.  
  Use a common template (e.g., `tool_output.html`) to display the output or error messages.

- **Data Flow:**  
  The frontend sends a POST request with the required data (for example, form data). The view calls the corresponding function from the AI tool file, obtains a result (a string), and then passes that result to the template for rendering.

### 4. Error Handling

- Ensure to check that all required inputs are provided.  
- Validate JSON data (for study planner inputs) and handle conversion errors.  
- Return clear error messages if any input is missing or invalid.

## Additional Notes

- Use Django’s built-in messaging framework if you want to display flash messages for success or error notifications.
- Comment your code to explain each step so that the integration is clear for future maintenance.
- Test each view thoroughly to ensure the correct functioning of the tool functions before integrating with the frontend.

This documentation should help you quickly integrate the functions from our AI tools and deliver the expected output to the frontend. If you encounter any issues or have questions, please reach out for clarification.
```

Feel free to copy and share this with Dev1 and Dev2 for integrating the AI tool functions into the Django project.