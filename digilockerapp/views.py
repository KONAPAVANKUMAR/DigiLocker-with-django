from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.contrib import messages

from digilockerapp.models import DocumentModel
# Create your views here.
def landingpageview(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    return render(request,"digilockerapp/index.html")

def loginpageview(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    return render(request,"digilockerapp/login.html")

def authenticateuser(request):
    username = request.POST['username']
    password = request.POST['password']
    print(username,password)
    user = authenticate(username = username,password = password)
    if user:
        login(request,user)
        return redirect('homepage')
    else:
        messages.add_message(request,messages.ERROR,"Invalid Credentials")
        return redirect(request.META['HTTP_REFERER'])

def logoutuser(request):
    logout(request)
    return redirect('landingpage')

def signupview(request):
    return render(request,"digilockerapp/signup.html")

def signup(request):
    username = request.POST['username']
    password = request.POST['password']
    repassword = request.POST['repassword']
    if password == repassword:
        if  not User.objects.filter(username = username).exists():
            User.objects.create_user(username = username,password = password).save()
            messages.add_message(request,messages.SUCCESS,"User succesfully created")
            return redirect("loginpage")
        else:
            messages.add_message(request,messages.ERROR,"Username already exists")
            return redirect(request.META['HTTP_REFERER'])
    else:
        messages.add_message(request,messages.ERROR,"Passwords not matched")
        return redirect(request.META['HTTP_REFERER'])
        
def homepageview(request):
    if not request.user.is_authenticated:
        return redirect('landingpage')
    user = request.user
    documents = DocumentModel.objects.filter(userid = user.id)
    context = {'user' : user,'documents':documents}
    return render(request,"digilockerapp/homepage.html",context)

def adddocumentview(request):
    return render(request,"digilockerapp/adddocument.html")

import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import pyAesCrypt
symmetricKey = "qwerpoiu"
def encrypt(fileName):
    pyAesCrypt.encryptFile(f'media/documents/{fileName}', f'media/encrypted/{fileName}', symmetricKey)
def decrypt(fileName):
    pyAesCrypt.decryptFile(f'media/encrypted/{fileName}', f'media/documents/{fileName}', symmetricKey)

def adddocument(request):
    title = request.POST['title']
    file = request.FILES['file']
    documentsUrl = os.path.join(settings.MEDIA_URL, 'documents/')
    documentsRoot = os.path.join(settings.MEDIA_ROOT, 'documents/')
    fs = FileSystemStorage(location=documentsRoot)
    filename = fs.save(file.name, file)
    uploaded_file_url = documentsUrl+filename
    encrypt(filename)
    DocumentModel(userid = request.user.id,title = title,file = f'documents/{filename}').save()
    decrypt(filename)
    messages.add_message(request,messages.INFO,"Document Added Succesfully")
    return redirect('homepage')

def deletedocument(request,id):
    DocumentModel.objects.get(id = id).delete()
    return redirect(request.META['HTTP_REFERER'])
