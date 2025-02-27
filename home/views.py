from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import ContactMessage, Policy
from aitool import optimise, research, studyplan, tutor  # Make sure studyplan and tutor are imported
# from aitool.tutor import solve_math_problem  # Add this import statement

def landing_index(request):
    if request.method == 'POST':
        # Extract the contact form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message_text = request.POST.get('message')
        # Save the data into the ContactMessage model
        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message_text
        )
        messages.success(request, 'Your message has been sent. Thank you!')
        return redirect('home')
    return render(request, 'iLanding/index.html')

def home(request):
    return render(request, 'home.html')

def terms_of_service(request):
    terms = get_object_or_404(Policy, policy_type='tos')
    return render(request, 'policies/terms.html', {'terms': terms})

def privacy_policy(request):
    privacy = get_object_or_404(Policy, policy_type='privacy')
    return render(request, 'policies/privacy_policy.html', {'privacy': privacy})

def cookies_policy(request):
    cookies = get_object_or_404(Policy, policy_type='cookies')
    return render(request, 'policies/cookies.html', {'cookies': cookies})

def researcher(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        response = research.fba_researcher(query)
        return render(request, 'tools/research.html', {'response': response})
    return render(request, 'tools/research.html')

# def planner(request):
#     if request.method == 'POST':
#         subjects_list = request.POST.getlist('subject[]')
#         exam_dates_list = request.POST.getlist('exam_date[]')
#         subjects = {}
#         for subj, date in zip(subjects_list, exam_dates_list):
#             if subj and date:
#                 subjects[subj] = date
#         extra_details = request.POST.get('extra_details', '')
#         study_plan = studyplan.generate_study_plan(subjects, extra_details)
#         return render(request, 'tools/planner.html', {'study_plan': study_plan})
#     return render(request, 'tools/planner.html')

# def tutor(request):
#     if request.method == 'POST':
#         question = request.POST.get('question')
#         tutor_response = solve_math_problem(question)  # use ask_question, not solve_math_problem
#         return render(request, 'tools/tutor.html', {'tutor_response': tutor_response})
#     return render(request, 'tools/tutor.html')

from .models import CodeSession, CodeMessage

def codeoptimiser(request):
    # Load the session history for the logged-in user (if any)
    optimized_history = CodeSession.objects.filter(user=request.user).order_by('-last_activity') if request.user.is_authenticated else []
    current_session = None
    conversation_messages = []

    if request.user.is_authenticated and 'current_session_id' in request.session:
        try:
            current_session = CodeSession.objects.get(id=request.session['current_session_id'], user=request.user)
            conversation_messages = current_session.messages.all().order_by('timestamp')
        except CodeSession.DoesNotExist:
            current_session = None

    if request.method == 'POST':
        code_snippet = request.POST.get('code_snippet')
        # You can also process the file if provided
        optimized_code = optimise.optimize_code(code_snippet)
        # Save the conversation if user is authenticated and a session is active
        if request.user.is_authenticated:
            if not current_session:
                # If no current session, create one with a default name
                current_session = CodeSession.objects.create(user=request.user, name="Default Session")
                request.session['current_session_id'] = current_session.id
            CodeMessage.objects.create(session=current_session, sender='user', text=code_snippet)
            CodeMessage.objects.create(session=current_session, sender='system', text=optimized_code)
            # Refresh conversation messages
            conversation_messages = current_session.messages.all().order_by('timestamp')
        return render(request, 'tools/codeoptimiser.html', {
            'optimized_code': optimized_code,
            'conversation_messages': conversation_messages,
            'current_session': current_session,
            'optimized_history': optimized_history,
        })
    return render(request, 'tools/codeoptimiser.html', {
        'conversation_messages': conversation_messages,
        'current_session': current_session,
        'optimized_history': optimized_history,
    })

def create_session(request):
    if request.method == 'POST':
        session_name = request.POST.get('session_name')
        if request.user.is_authenticated:
            new_session = CodeSession.objects.create(user=request.user, name=session_name)
            request.session['current_session_id'] = new_session.id
            return redirect('codeoptimiser')
        else:
            messages.error(request, "Please log in to create a session.")
            return redirect('login')
    return redirect('codeoptimiser')

def load_session(request, session_id):
    if request.user.is_authenticated:
        try:
            session = CodeSession.objects.get(id=session_id, user=request.user)
            request.session['current_session_id'] = session.id
        except CodeSession.DoesNotExist:
            messages.error(request, "Session not found.")
    return redirect('codeoptimiser')

from django.http import HttpResponse
from .models import StudySession, StudyMessage

def studyplanner(request):
    # Load study planner session history for the logged-in user (if any)
    study_history = StudySession.objects.filter(user=request.user).order_by('-last_activity') if request.user.is_authenticated else []
    current_session = None
    conversation_messages = []

    if request.user.is_authenticated and 'current_study_session_id' in request.session:
        try:
            current_session = StudySession.objects.get(id=request.session['current_study_session_id'], user=request.user)
            conversation_messages = current_session.messages.all().order_by('timestamp')
        except StudySession.DoesNotExist:
            current_session = None

    if request.method == 'POST':
        # Get subjects and exam dates from the form
        subjects_list = request.POST.getlist('subject[]')
        exam_dates_list = request.POST.getlist('exam_date[]')
        subjects = {}
        for subj, date in zip(subjects_list, exam_dates_list):
            if subj and date:
                subjects[subj] = date
        extra_details = request.POST.get('extra_details', '')
        # Generate study plan using your Gemini-based function
        study_plan = studyplan.generate_study_plan(subjects, extra_details)

        # Save conversation if the user is authenticated
        if request.user.is_authenticated:
            if not current_session:
                # Create a new default session if none exists
                current_session = StudySession.objects.create(user=request.user, name="Default Study Session")
                request.session['current_study_session_id'] = current_session.id
            # Save user input and generated study plan as messages
            StudyMessage.objects.create(
                session=current_session,
                sender='user',
                text="Subjects: " + str(subjects) + "\nExtra Details: " + extra_details
            )
            StudyMessage.objects.create(
                session=current_session,
                sender='system',
                text=study_plan
            )
            conversation_messages = current_session.messages.all().order_by('timestamp')
        return render(request, 'tools/studyplanner.html', {
            'study_plan': study_plan,
            'conversation_messages': conversation_messages,
            'current_session': current_session,
            'study_history': study_history,
        })

    return render(request, 'tools/studyplanner.html', {
        'conversation_messages': conversation_messages,
        'current_session': current_session,
        'study_history': study_history,
    })

def create_study_session(request):
    if request.method == 'POST':
        session_name = request.POST.get('session_name')
        if request.user.is_authenticated:
            new_session = StudySession.objects.create(user=request.user, name=session_name)
            request.session['current_study_session_id'] = new_session.id
            return redirect('studyplanner')
        else:
            messages.error(request, "Please log in to create a study session.")
            return redirect('login')
    return redirect('studyplanner')

def load_study_session(request, session_id):
    if request.user.is_authenticated:
        try:
            session = StudySession.objects.get(id=session_id, user=request.user)
            request.session['current_study_session_id'] = session.id
        except StudySession.DoesNotExist:
            messages.error(request, "Study session not found.")
    return redirect('studyplanner')

def download_study_plan(request, session_id):
    # Dummy implementation: In production, generate a PDF from the study plan HTML.
    session = get_object_or_404(StudySession, id=session_id, user=request.user)
    # Assume the latest system message holds the study plan
    study_plan_msg = session.messages.filter(sender='system').last()
    if study_plan_msg:
        content = study_plan_msg.text
    else:
        content = "No study plan available."
    response = HttpResponse(content, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="study_plan.pdf"'
    # Here you would integrate PDF generation logic.
    response.write("PDF Content:\n" + content)
    return response

from .models import WorksheetSession, WorksheetMessage
from aitool import tutor  # tutor.py provides solve_math_problem and generate_worksheet

def tutor_view(request):
    # Default active tab is "solve". You can pass active_tab in context.
    active_tab = request.POST.get('mode', 'solve')  # mode is 'solve' or 'worksheet'
    
    context = {'active_tab': active_tab}
    
    # For "solve" mode, use your existing tutor logic:
    if request.method == 'POST' and active_tab == 'solve':
        question = request.POST.get('question')
        tutor_response = tutor.solve_math_problem(question)
        context['tutor_response'] = tutor_response

    # For "worksheet" mode, process worksheet generation:
    if request.method == 'POST' and active_tab == 'worksheet':
        topic = request.POST.get('topic')
        num_questions = request.POST.get('num_questions', 5)
        # Generate worksheet using your tutor function:
        worksheet_output = tutor.generate_worksheet(topic, num_questions)
        context['worksheet_output'] = worksheet_output
        # If user is authenticated, save the worksheet conversation in a session:
        if request.user.is_authenticated:
            current_ws_session = None
            if 'current_worksheet_session_id' in request.session:
                try:
                    current_ws_session = WorksheetSession.objects.get(id=request.session['current_worksheet_session_id'], user=request.user)
                except WorksheetSession.DoesNotExist:
                    current_ws_session = None
            if not current_ws_session:
                current_ws_session = WorksheetSession.objects.create(user=request.user, name="Default Worksheet Session")
                request.session['current_worksheet_session_id'] = current_ws_session.id
            WorksheetMessage.objects.create(session=current_ws_session, sender='user', text=f"Topic: {topic}, Questions: {num_questions}")
            WorksheetMessage.objects.create(session=current_ws_session, sender='system', text=worksheet_output)
            context['current_worksheet_session'] = current_ws_session
            context['worksheet_history'] = WorksheetSession.objects.filter(user=request.user).order_by('-last_activity')
    
    return render(request, 'tools/tutor.html', context)

def create_worksheet_session(request):
    if request.method == 'POST':
        session_name = request.POST.get('session_name')
        if request.user.is_authenticated:
            new_session = WorksheetSession.objects.create(user=request.user, name=session_name)
            request.session['current_worksheet_session_id'] = new_session.id
            return redirect('tutor')
        else:
            messages.error(request, "Please log in to create a worksheet session.")
            return redirect('login')
    return redirect('tutor')

def load_worksheet_session(request, session_id):
    if request.user.is_authenticated:
        try:
            session = WorksheetSession.objects.get(id=session_id, user=request.user)
            request.session['current_worksheet_session_id'] = session.id
        except WorksheetSession.DoesNotExist:
            messages.error(request, "Worksheet session not found.")
    return redirect('tutor')

def download_worksheet(request, session_id):
    # Dummy PDF download implementation; integrate an actual PDF generator as needed.
    session = get_object_or_404(WorksheetSession, id=session_id, user=request.user)
    worksheet_msg = session.messages.filter(sender='system').last()
    content = worksheet_msg.text if worksheet_msg else "No worksheet available."
    response = HttpResponse(content, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="worksheet.pdf"'
    response.write("PDF Content:\n" + content)
    return response

from .models import ResearchSession, ResearchMessage
from aitool import research  # research.fba_researcher is available

def research_view(request):
    # Load research session history for the logged-in user (if any)
    research_history = ResearchSession.objects.filter(user=request.user).order_by('-last_activity') if request.user.is_authenticated else []
    current_session = None
    conversation_messages = []

    if request.user.is_authenticated and 'current_research_session_id' in request.session:
        try:
            current_session = ResearchSession.objects.get(id=request.session['current_research_session_id'], user=request.user)
            conversation_messages = current_session.messages.all().order_by('timestamp')
        except ResearchSession.DoesNotExist:
            current_session = None
  
    if request.method == 'POST':
        # Read the research query input
        query_text = request.POST.get('query', '')
        # Process file attachment if provided
        research_file = request.FILES.get('research_file')
        file_content = ""
        if research_file:
            # NOTE: For real extraction, integrate a library (like PyPDF2 for PDF or python-docx for DOC)
            try:
                file_content = research_file.read().decode('utf-8', errors='ignore')
            except Exception as e:
                file_content = f"Error reading file: {e}"
        # Combine file content and query (if both provided)
        input_message = (file_content + "\n" + query_text).strip()
        if not input_message:
            messages.error(request, "Please attach a file or enter a query.")
            return redirect('researcher')
        # Call the researcher function – it returns a JSON response; here we convert it to plain text for display.
        response = research.fba_researcher(input_message)
        # For simplicity, we assume response is a text string (or you may parse the JSON as needed)
        research_response = response  # adjust if needed

        # Save the conversation if the user is authenticated
        if request.user.is_authenticated:
            if not current_session:
                current_session = ResearchSession.objects.create(user=request.user, name="Default Research Session")
                request.session['current_research_session_id'] = current_session.id
            ResearchMessage.objects.create(session=current_session, sender='user', text=input_message)
            ResearchMessage.objects.create(session=current_session, sender='system', text=research_response)
            conversation_messages = current_session.messages.all().order_by('timestamp')
        return render(request, 'tools/research.html', {
            'research_response': research_response,
            'conversation_messages': conversation_messages,
            'current_session': current_session,
            'research_history': research_history,
        })

    return render(request, 'tools/research.html', {
        'conversation_messages': conversation_messages,
        'current_session': current_session,
        'research_history': research_history,
    })

def create_research_session(request):
    if request.method == 'POST':
        session_name = request.POST.get('session_name')
        if request.user.is_authenticated:
            new_session = ResearchSession.objects.create(user=request.user, name=session_name)
            request.session['current_research_session_id'] = new_session.id
            return redirect('researcher')
        else:
            messages.error(request, "Please log in to create a research session.")
            return redirect('login')
    return redirect('researcher')

def load_research_session(request, session_id):
    if request.user.is_authenticated:
        try:
            session = ResearchSession.objects.get(id=session_id, user=request.user)
            request.session['current_research_session_id'] = session.id
        except ResearchSession.DoesNotExist:
            messages.error(request, "Research session not found.")
    return redirect('researcher')

def download_research(request, session_id):
    # Dummy implementation: For a production-ready PDF, integrate a PDF generator.
    session = get_object_or_404(ResearchSession, id=session_id, user=request.user)
    research_msg = session.messages.filter(sender='system').last()
    content = research_msg.text if research_msg else "No research output available."
    response = HttpResponse(content, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="research_output.pdf"'
    response.write("PDF Content:\n" + content)
    return response
