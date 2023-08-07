from django.shortcuts import render, redirect
from .models import user_details, admin, user_appointments, customers
from django.contrib import messages
import random


def landing(request):
    return render(request, 'landing-page.html')


def home(request):
    return render(request, 'home.html')


def services(request):
    return render(request, 'services.html')


def about(request):
    return render(request, 'about.html')


def login(request):
    return render(request, 'login.html')


def dashboard(request):
    return render(request, 'admin_dashboard.html')


def new(request):
    return render(request, 'admin_dashboard/new_appointments.html')


def accepted(request):
    return render(request, 'admin_dashboard/accepted_appointments.html')


def rejected(request):
    return render(request, 'admin_dashboard/rejected_appointments.html')


def invoice(request):
    return render(request, 'admin_dashboard/invoices.html')


def search_invoice(request):
    return render(request, 'admin_dashboard/search_invoice.html')


def contacts(request):
    return render(request, 'contacts.html')


def admin_login(request):
    return render(request, 'login-admin.html')


def logincon(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        try:
            user = user_details.objects.get(emailid=username)
            if user.password == password:
                return redirect('/home')
            else:
                messages.error(
                    request, 'Incorrect username or password. Please try again.')
                return redirect('/login')
        except user_details.DoesNotExist:
            messages.error(request, 'User not found. Please check your email.')
            return redirect('/login')

    return render(request, 'login.html')


def signup(request):
    username = request.POST['username1']
    password = request.POST['password1']
    email = request.POST['email1']

    try:
        user = user_details(username=username,
                            password=password, emailid=email)
        user.save()
        return redirect('/login')
    except:
        return redirect('/login')


def adminsignin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = admin.objects.get(username=username)
            if user.password == password:
                return redirect('/admin-dashboard')
            else:
                messages.error(
                    request, 'Incorrect password. Please try again.')
                return redirect('/admin-login')
        except admin.DoesNotExist:
            messages.error(
                request, 'Username not found. Please check your username.')
            return redirect('/admin-login')

    return render(request, 'admin_login.html')


def generate_appointment_number():
    return random.randint(1000, 9999)


def appointment_details(request):
    if request.method == 'POST':
        service = request.POST.get('service', '')
        name = request.POST.get('name', '')
        phone = request.POST.get('phone', '')
        date = request.POST.get('date', '')
        time = request.POST.get('time', '')

        while True:
            appointment_number = generate_appointment_number()

            # Check if the generated appointment number already exists
            if not user_appointments.objects.filter(appointment_number=appointment_number).exists():
                break

        # Create and save the appointment object to the database
        appointment = user_appointments(
            service=service, name=name, phone=phone, date=date, time=time, appointment_number=appointment_number)
        appointment.save()

        # Return a response indicating successful form submission (you can customize this)
        return redirect('/services')


def display_appointments(request):
    # Retrieve customer data from the database
    appointments = customers.objects.all()

    context = {
        'appointments': appointments
    }

    return render(request, 'admin_dashboard/customer.html', context)


def display_all(request):
    appointments = user_appointments.objects.all()
    context = {
        'appointments': appointments
    }

    return render(request, 'admin_dashboard/all_appointments.html', context)


def appointments(request):
    appointments = user_appointments.objects.all().values(
        'appointment_number', 'service', 'date', 'time'
    )
    context = {
        'appointments': appointments
    }
    return render(request, 'appointments.html', context)


def search_appointment(request):
    return render(request, 'admin_dashboard/search_appointment.html')


def search_appointment1(request):
    appointment = None
    no_records_found = False

    if request.method == 'POST':
        appointment_number = request.POST.get('appointment-number', '')
        try:
            appointment = user_appointments.objects.get(
                appointment_number=appointment_number)
        except user_appointments.DoesNotExist:
            no_records_found = True

    return render(request, 'admin_dashboard/search_appointment.html', {'appointment': appointment, 'no_records_found': no_records_found})
