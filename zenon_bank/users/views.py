from django.shortcuts import render, redirect
from .forms import UserForm, StudentCreationForm
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.conf import settings
from .models import Student
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm, StudentUpdateForm
from files.models import File


def signup(request):

    if request.method == "POST":
        u_form = UserForm(request.POST)
        s_form = StudentCreationForm(request.POST)  
        


        if u_form.is_valid():

                #create a user account but deactivate it
                user = u_form.save(commit=False)
                user.is_active = False
                user.save()
                
                
                #create a student object to accompany the created user object
                student = s_form.save(commit=False)
                student.user = user
                student.save()

                #contstructing and sending confirmation email
                current_site = get_current_site(request)
                mail_subject = "Activate Your Zenon Bank Account"
                messege = render_to_string("users/account_activation.html", {                        
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                })

                    
                to_email = u_form.cleaned_data.get("email")
                email = EmailMessage(
                    subject=mail_subject,
                    body=messege,
                    from_email=settings.EMAIL_HOST_USER,
                    to=[to_email],
                )

                email.send()
                    
                #TODO: replace with proper redirect once finished
                messages.success(request, f"A vertification email has been sent to {to_email}\n vertify your email address to qualify for login")
                return redirect("signup")
                

    else:       
        u_form = UserForm()
        s_form = StudentCreationForm()
            
    context = {"u_form": u_form, "s_form": s_form}
    return render(request, "users/signup.html", context)


def activate(request, uidb64, token):

    try:
        uid =force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect("home")
    
    else: return HttpResponse("Activation link is invalid")

@login_required
def logout(request):
    auth_logout(request)
    template_name = 'registration/logged_out.html'
    return render(request, template_name=template_name)


@login_required
def profile(request):

    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        student_form = StudentUpdateForm(request.POST, instance=request.user.student)

        if user_form.is_valid() and profile_form.is_valid() and student_form.is_valid():
            user_form.save()
            profile_form.save()
            student_form.save()

            messages.success(request, "Account Updated Successfully")
            return redirect("profile")
    
    else:
        user_form = UserUpdateForm( instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        student_form = StudentUpdateForm(instance=request.user.student)
        accepted_files = File.objects.filter(student=request.user, state=File.accepted)
        pending_files = File.objects.filter(student=request.user, state=File.pending)
        denied_files = File.objects.filter(student=request.user, state=File.denied)



    context = {
        
        "accepted_files" : accepted_files,
        "pending_files" : pending_files,
        "denied_files" : denied_files,
        "u_form" : user_form,
        "p_form" : profile_form,
        "s_form" : student_form,

    }

    template_name = "users/profile.html"
    return render(request, template_name=template_name, context=context)