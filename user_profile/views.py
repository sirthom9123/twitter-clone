import json
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.contrib import auth
from django.template.loader import render_to_string
from django.views.generic import View
from django.template import Context
from django.core.mail import EmailMessage
from django.utils.encoding import force_text, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.conf import settings
import threading
import random
import string

from .models import Invitation
from .forms import InvitationForm
from .utils import token_generator


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)
        
    def run(self):
        self.email.send(fail_silently=False)


# Validation Views for Email and Username.
class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': 'Email invalid'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'It seems this email is registered. Try forgot Password?'}, status=409)
        return JsonResponse({'username_valid': True})

class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'Username should only contain alphanumeric characters'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Sorry username in use, choose another one.'}, status=409)
        return JsonResponse({'username_valid': True})
    
    
# register view    
class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')
    
    def post(self, request):
        
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        context = {'fieldValues':request.POST}
        
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'Password length is too short')
                    return render(request, 'authentication/register.html', context)
                
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()
                
                
                domain = get_current_site(request).domain
                email_body = {
                    'user': user,
                    'domain': domain.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': token_generator.make_token(user),
                }

                link = reverse('activate', kwargs={
                        'uidb64': email_body['uid'], 'token': email_body['token']})
                
                activate_url = 'http://'+domain+link
                email_subject = 'Activate your account'
                email_body = 'Hi ' + user.username + ' Please use this link to verfiy your account\n' + activate_url
                emailTo = request.POST['email']
                email = EmailMessage(
                        email_subject,
                        email_body,
                        settings.EMAIL_HOST_USER,
                        [emailTo],                        
                    )
                EmailThread(email).start()
                messages.success(request, 'Account created successfully')
                return render(request, 'authentication/register.html')
                
        return render(request, 'authentication/register.html')
        
        
class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)
            
            if not token_generator.check_token(user, token):
                return redirect('login' + '?message=' + 'User already activated')
            
            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()
            
            messages.success(request, 'Account activated successfully')
            return redirect('login')
        
        except Exception as ex:
            pass
        
        return redirect('login')
    
    
class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(request, username=username, password=password)
            
            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Welcome, ' + user.username + ' you are now logged in!')
                    return redirect('index')
                
                messages.error(request, 'Account is not activated, please check your email!')    
                return render(request, 'authentication/login.html')
           
            messages.error(request, 'Invalid credentials, try again!')    
            return render(request, 'authentication/login.html')
        
        
        messages.error(request, 'Please fill all fields!')    
        return render(request, 'authentication/login.html')
        
        
        
class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You have been logged out')
        return redirect('login')
    
    
class RequestPasswordResetEmail(View):
    def get(self, request):
        
        return render(request, 'authentication/reset_password.html')
    
    
    def post(self, request):
        email = request.POST['email']
        
        context = {'values': request.POST}
        if not validate_email(email):
            messages.error(request, 'Please supply valid email') 
            return render(request, 'authentication/reset_password.html', context)
        
        domain = get_current_site(request).domain
        user = User.objects.filter(email=email)
        if user.exists():
            email_contents = {
            'user': user,
            'domain': domain,
            'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
            'token': PasswordResetTokenGenerator().make_token(user[0]),
        }

            link = reverse('reset_user_password', kwargs={
                            'uidb64': email_contents['uid'], 'token': email_contents['token']})
            
            reset_url = 'http://'+domain+link
            email_subject = 'Password Reset'
            email_body = 'Hi there\n. Please use this link to reset your password\n' + reset_url
            emailTo = request.POST['email']
            email = EmailMessage(
                    email_subject,
                    email_body,
                    settings.EMAIL_HOST_USER,
                    [emailTo],                        
                )
            EmailThread(email).start()
        messages.success(request, 'We have sent you an email to reset your password.')
        
        return render(request, 'authentication/reset_password.html', context)
        
        
        
        
class CompletePasswordReset(View):
    def get(self, request, uidb64, token): 
        context = {'uidb64': uidb64, 'token': token}
        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
            
                messages.info(request, 'Password reset link has been used, please request a new link!')
                return redirect('password_reset')
            
        except Exception as identifier:
            pass
        return render(request, 'authentication/set_new_password.html', context)
    
    def post(self, request, uidb64, token): 
        context = {'uidb64': uidb64, 'token': token}
        
        password = request.POST['password']
        password2 = request.POST['password2']
        if password != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'authentication/set_new_password.html', context)
        if len(password) < 6:
            messages.error(request, 'Password too short.')
            return render(request, 'authentication/set_new_password.html', context)
        
        
        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(request, 'Passwrod reset successful. You can login with new password!')
            return redirect('login')
            
        except Exception as identifier:
            messages.info(request, 'Something went wrong')
            return render(request, 'authentication/set_new_password.html', context)
            
        
def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))

        
class Invite(View):
    def get(self, request):
        success = request.GET.get('success')
        email = request.GET.get('email')
        invite = InvitationForm()
        context = {'success': success, 'invite': invite, 'email': email}
        return render(request, 'tweets/email.html', context)
    
    def post(self, request):
        form = InvitationForm(self.request.POST)
        user = User.objects.get(username=request.user.username)
        
        if form.is_valid():
            domain = get_current_site(request).domain
            email = form.cleaned_data['email']
            subject = 'Invitation to join MyTweet App'
            sender_name = request.user.username
            sender_email = request.user.email
            invite_code = create_ref_code()
            invite_url = f'http://{domain}/authenticate/register/'
            
            context = {'sender_name': sender_name, 'sender_email': sender_email, 'email': email, 'link': invite_url}
            invite_body = render_to_string('partials/_invite_email_template.html', context)
            msg = EmailMessage(subject, 
                               invite_body, 
                               settings.EMAIL_HOST_USER, 
                               [email], 
                               cc=[settings.EMAIL_HOST_USER]
                               )
            
            invitation = Invitation()
            invitation.email = email
            invitation.code = invite_code
            invitation.sender = user
            invitation.save()
            EmailThread(msg).start()
            messages.success(self.request, f'Invitation sent to {email}.')
            return HttpResponseRedirect('/')