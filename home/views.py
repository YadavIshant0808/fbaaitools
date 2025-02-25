from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import ContactMessage, Policy
#import files from ai tools take help of gpt 

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

        # Display a success message and redirect (you can redirect back to the contact section)
        messages.success(request, 'Your message has been sent. Thank you!')
        return redirect('home')  # or use redirect('contact') if you prefer

    # Render the landing page (located at templates/landing/index.html)
    return render(request, 'iLanding/index.html')
def home(request):
    return render(request, 'home.html')

def terms_of_service(request):
    terms = get_object_or_404(Policy, policy_type='tos')
    return render(request, 'policies/terms', {'terms': terms})

def privacy_policy(request):
    privacy = get_object_or_404(Policy, policy_type='privacy')
    return render(request, 'policies/privacy_policy.html', {'privacy': privacy})

def cookies_policy(request):
    cookies = get_object_or_404(Policy, policy_type='cookies')
    return render(request, 'policies/cookies.html', {'cookies': cookies})

def researcher(request):
    return render(request, 'tools/researcher.html') #Aditya complete this function to render the researcher.html template take help of chat gpt  

def planner(request):
    return render(request, 'tools/planner.html')#Aditya complete this function to render the researcher.html template take help of chat gpt  

def tutor(request):
    return render(request, 'tools/tutor.html')#Ahem complete this function to render the researcher.html template take help of chat gpt  

#i have completed the function to render the tutor.html template to you how to do
def codeoptimiser(request):
    if request.method == 'POST': #same to other functions 
        code_snippet = request.POST.get('code_snippet')#same to other functions but variable should different
        optimized_code = optimize_code(code_snippet) # pass the variable to the function and function should be imported from ai tools
        return render(request, 'tools/codeoptimiser.html', {'optimized_code': optimized_code}) # render the template with the optimized code passing through context in dictionary
    return render(request, 'tools/codeoptimiser.html')#Ahem complete this function to render the researcher.html template take help of chat gpt  

