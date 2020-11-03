from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
import requests
import json

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created ! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'ticket/signup.html', {'form': form, 'title': 'reqister here'})

def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            form = login(request, user)
            messages.success(request, f' wecome {username} !!')
            return redirect('dashboard')
        else:
            messages.info(request, f'account done not exit plz sign in')
    form = AuthenticationForm()
    return render(request, 'ticket/login.html', {'form': form, 'title': 'login'})

@login_required(login_url='/login/')
def dashboard(request):
    global ticketNumber, status, subject, description
    u = User.objects.get(id=request.user.id)
    ticketid = u.profile.ticket_support_id

    auth_token = "9446933330c7f886fbdf168452906a9e0"
    org_id = "60001840952"

    ticket_id = str(ticketid)
    params = "include=contacts,products"

    headers = {
        "Authorization": auth_token,
        "orgId": org_id,
        "contentType": "application/json; charset=utf-8"
    }

    ticket_request = requests.get('https://desk.zoho.in/api/v1/tickets/' + ticket_id + '?' + params, headers=headers)

    if ticket_id:
        if ticket_request.status_code == 200:
            print("Request Successful,Response:")
            a = json.loads(ticket_request.content)
            ticketNumber = a["ticketNumber"]
            status = a["status"]
            subject = a["subject"]
            description = a["description"]
            print(a["ticketNumber"])
            print(a["status"])
            print(a["subject"])
            print(a["description"])
        else:
            print("Request not successful,Response code ", ticket_request.status_code, " \nResponse : ",ticket_request.content)
            ticketNumber = "TicketNumber"
            status = "status"
            subject = "subject"
            description = "description"

    check_id = u.profile.customer_id
    if check_id is not None:
        return render(request, 'ticket/dashboard.html', {"name": u,"ticketNumber":ticketNumber,"status":status, "subject": subject, "description":description})
    else:
        contact_data = {
            "lastName": u.last_name,
            "firstName": u.first_name,
            "email": u.email,
        }

        headers = {
            "Authorization": auth_token,
            "orgId": org_id,
            "contentType": "application/json; charset=utf-8"
        }
        request_api = requests.post('https://desk.zoho.in/api/v1/contacts', headers=headers,data=json.dumps(contact_data))

        if request_api.status_code == 200:
            print("Request Successful,Response:")
            a = json.loads(request_api.content)
            print(a['id'])
            u.profile.customer_id = a['id']
            u.profile.save()
        else:
            print("Request not successful,Response code ", request_api.status_code, " \nResponse : ",request_api.content)
        return render(request, 'ticket/dashboard.html', {"name": u,"ticketNumber":ticketNumber,"status":status, "subject": subject, "description":description})

@login_required(login_url='/login/')
def submit_ticket(request):
    global department,a
    department = []
    id =[]
    category = ["-None-","NEW Project CI/CD Pipeline Setup","Update CI/CD Pipeline Configuration","DevSecOps Pipeline Setup","CI/CD pipeline failure","others"]
    auth_token = "9446933330c7f886fbdf16745906a9e0"
    org_id = "60001287852"

    headers = {
        "Authorization": auth_token,
        "orgId": org_id,
        "contentType": "application/json; charset=utf-8"
    }
    request_api = requests.get('https://desk.zoho.in/api/v1/departments', headers=headers)

    if request_api.status_code == 200:
        print("Request Successful,Response:")
        a = json.loads(request_api.content)
        for i in a['data']:
            department.append(i['name'])
            id.append(i['id'])
    else:
        print("Request not successful,Response code ", request_api.status_code, " \nResponse : ", request_api.content)

    u = User.objects.get(id=request.user.id)
    if "GET" == request.method:
        return render(request, "ticket/forms.html",{"name": u,"email":u.email,"department":department,"category":category})
    if request.method == 'POST':
        u = User.objects.get(id=request.user.id)
        Contact_id = u.profile.customer_id
        Name = u,
        Email = u.email
        Department_name= request.POST.get("department")
        category = request.POST.get("category")
        subject = request.POST.get("subject")
        description = request.POST.get("description")
        priority = request.POST.get("priority")

        Department = [d['id'] for d in a['data'] if d['name'] == Department_name]

        ticket_data = {
            "email" : Email,
            "departmentId": "".join(Department),
            "contactId": Contact_id,
            "category": category,
            "subject": subject,
            "description" : description,
            "priority" : priority,
        }

        headers = {
            "Authorization": auth_token,
            "orgId": org_id,
            "contentType": "application/json; charset=utf-8"
        }

        ticekt_request = requests.post('https://desk.zoho.in/api/v1/tickets', headers=headers,data=json.dumps(ticket_data))

        if ticekt_request.status_code == 200:
            print("Request Successful,Response:")
            a = json.loads(ticekt_request.content)
            u.profile.ticket_support_id = a["id"]
            u.profile.save()
            print(a)
            messages.success(request, f' Ticket is Created')
        else:
            print("Request not successful,Response code ", ticekt_request.status_code, " \nResponse : ",ticekt_request.content)
            messages.info(request, f' Ticket is Not Created')
        return redirect('submit_form')
