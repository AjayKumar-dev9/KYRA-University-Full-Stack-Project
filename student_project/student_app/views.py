from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.http import JsonResponse
from .models import student_record
import random as r
import json

#generate otp
def generate_otp(length):
        start_range = 10**(length - 1)
        end_range = (10**length) - 1
        otp = r.randint(start_range, end_range)
        return otp

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # If behind a proxy
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def signup(request):
    otp_session = request.session.get('otp_code', '')
    if request.method == 'POST':

        if request.content_type == 'application/json':

            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({'success': False, 'error': 'Invalid Eamil'}, status=400)
            email_otp = data.get('email')
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            full_name = f"{first_name} {last_name}".strip()
            otp = data.get('otp') 
            check_type_email = data.get('for_email')
            check_type_otp = data.get('for_otp')

        
            if check_type_email == "for_email":
                    
                #create otp
                otp_length = 6 
                generated_otp = generate_otp(otp_length)
                request.session['otp_code'] = generated_otp

                if not first_name:
                    return JsonResponse({'success': False, 'error': 'First Name is Required'})
                elif not last_name:
                    return JsonResponse({'success': False, 'error': 'Last Name is Required'})
                elif not email_otp:
                    return JsonResponse({'success': False, 'error': 'Eamil is Required'})
                else:
                    if User.objects.filter(email=email_otp).exists() or student_record.objects.filter(email=email_otp).exists():
                        return JsonResponse({'success': False, 'error': 'Email already registered.'})
                    else:
                        # Send OTP
                        subject = 'Email verification for Registration'
                        message = f'Hello {full_name},\n\nOTP: {generated_otp}\n\nThis code is valid for 10 minutes. Please do not share it with anyone.\n\nThank you for registering!'
                        from_email = settings.EMAIL_HOST_USER
                        recipient_list = [email_otp]

                        send_mail(subject, message, from_email, recipient_list)
                        return JsonResponse({'success': True, 'message': 'OTP sent successfully. Check your mail for OTP'})



            if check_type_otp == 'for_otp':
                if not otp:
                    return JsonResponse({'success': False, 'error': 'OTP is Required'})
                else:
                    if int(otp) == otp_session:
                        del request.session['otp_code']
                        return JsonResponse({'success': True, 'message': 'OTP Verified.'})
                    else:
                        return JsonResponse({'success': False, 'error': 'OTP Mismatch.'})
                           
        else:

            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            full_name = f"{first_name} {last_name}".strip()


            if not username or not password:
                messages.error(request, "Username and password are required.")
            elif User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.choose differntly")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered.")
            else:
                User.objects.create_user(username=username,password=password,email=email,first_name=first_name,last_name=last_name)
                # Send email
                subject = 'Welcome to KYRA University – Registration Successful 🎓'
                message = f'Dear {full_name},\n\nWelcome to KYRA University!\n\nYour registration was successful. You can now log in and explore all the features and opportunities we offer.\n\nIf you have any questions or need help, feel free to reach out.\n\nBest regards,\nKYRA University Team\nsupport@kyrauniversity.com'
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [email]

                send_mail(subject, message, from_email, recipient_list)
                return redirect('login')

    return render(request,'signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username or not password:
            messages.error(request, "Username and password are required.")
        else:
            if User.objects.filter(email=username).exists():
                user_obj = User.objects.get(email=username)
                username = user_obj.username
            else:
                username = username
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request,user)

                name = user.first_name
                email = user.email

                timestamp = timezone.now().strftime('%d %B %Y, %I:%M %p')
                ip_address = get_client_ip(request)
                # Send email
                subject = 'Login Alert: You just signed in to KYRA University'
                message = f'Hi {name},\n\nWe noticed a login to your KYRA University account.\n\n🕒 Time: { timestamp }\n📍 IP Address: { ip_address }\n\nIf this was you, you can safely ignore this message.\nIf not, we recommend changing your password immediately for security.\n\nBest,\nKYRA University Security Team.'
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [email]

                send_mail(subject, message, from_email, recipient_list)
                return redirect('home')
            else:
                messages.error(request, "Invalid credentials.")

    return render(request,'login.html')
def home(request):
    if request.user.is_authenticated:
        user_email = request.user.email
        try:
            student_email = student_record.objects.get(email=user_email)
            if user_email == student_email.email:
                return render(request, 'home.html', {'Student': student_email})
        except student_record.DoesNotExist:
            # User exists but no student_form record — show home or redirect to fill the form
            return render(request, 'home.html', {'Student': None})
    else:
        return render(request, 'home.html')

def logout_view(request):
    if request.method == 'POST':
        logout(request)  
        return redirect('home')
    else:
        return redirect('home')


def forgot_password(request):
    email_username = request.session.get('email_username', '')
    otp_session = request.session.get('otp_code', '')
    if request.method == 'POST':
        
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({'success': False, 'error': 'Invalid Eamil'}, status=400)
            
            email = data.get('email')
            user_otp = data.get('otp')
            check_type_email = data.get('for_email')
            check_type_otp = data.get('for_otp')
            print(check_type_email)

            if check_type_email == "for_email":
                print('name')
                if not email:
                    return JsonResponse({'success':False,'error':'Email is Required.'})
                else:
                    try:
                        get_emil = User.objects.filter(email=email).exists()
                        name = User.objects.get(email=email)
                        request.session['email_username'] = email
                        if str(get_emil) == 'True':
                            otp_length = 6 
                            generated_otp = generate_otp(otp_length)
                            request.session['otp_code'] = generated_otp

                            subject = 'Your One-Time Password (OTP) – KYRA University'
                            message = f'Hello {name} ,\n\nOTP: {generated_otp}\nThis code is valid for 10 minutes. Please do not share it with anyone.\n\nThank you for registering!'
                            from_email = settings.EMAIL_HOST_USER
                            recipient_list = [email]

                            send_mail(subject, message, from_email, recipient_list)
                            return JsonResponse({'success': True, 'message': 'OTP send successfully. Check in your mail for OTP'})
                    except User.DoesNotExist:
                        return JsonResponse({'success':False,'error':'Email not register.'})   
            elif check_type_otp == 'for_otp':
                if not user_otp:
                    return JsonResponse({'success':False,'error':'OTP is requried'})             
                elif int(user_otp) == otp_session:
                    return JsonResponse({"success": True, "redirect_url": "/newpassword/"})
                else:
                    return JsonResponse({'success':False,'error':'OTP is Mismatch'}) 
    return render(request,'forgot_password.html')

def new_password(request):
    email_username = request.session.get('email_username')
    if request.method == 'POST':
        new_pass = request.POST.get('new_pass')
        conf_new_pass = request.POST.get('conform_new_password')

        if new_pass == conf_new_pass and email_username:
            try:
                user = User.objects.get(email=email_username)
                user.password = make_password(new_pass)
                user.save()
                del request.session['email_username']
                del request.session['otp_code']
                messages.success(request, "Password reset successful. Please log in.")
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, "Something went wrong.")
        else:
            messages.error(request,"Passwords did't match.")


    return render(request,'new_password.html')

def student_form(request):

    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        date_of_birth = request.POST.get('date_of_birth')
        gender = request.POST.get('gender')
        graduation = request.POST.get('graduation')
        course = request.POST.get('course')
        image = request.FILES.get('image')


        
        record = student_record(first_name=first_name,last_name=last_name,ph_no=phone,email=email,dob=date_of_birth,gender=gender,graduation_completed=graduation,course=course,image=image)
        record.save()
        return redirect('success')
    return render(request,'student_form.html')

def sucess(request):
    return render(request,'success_page.html')

def profile(request):
    if request.user.is_authenticated:
        user_email = request.user.email
        student_email = student_record.objects.get(email=user_email)
        if user_email == student_email.email:
            return render(request, 'profile.html', {'Student':student_email} )
    else:
        return render(request, 'home.html')

def edit_profile(request):
    if request.user.is_authenticated:
        user_email = request.user.email
        student = get_object_or_404(student_record, email=user_email)

        if request.method == "POST":
            student.first_name = request.POST.get("first_name")
            student.last_name = request.POST.get("last_name")
            student.ph_no = request.POST.get("phone")
            student.dob = request.POST.get("date_of_birth")
            student.gender = request.POST.get("gender")
            student.graduation_completed = request.POST.get("graduation")
            student.course = request.POST.get("course")

            if request.FILES.get("image"):
                student.image = request.FILES.get("image")

            student.save()
            return redirect("profile")

    return render(request, "edit_profile.html", {"student": student})

def test(request):
    return render(request,'test.html')