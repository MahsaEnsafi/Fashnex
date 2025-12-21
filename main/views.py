from django.shortcuts import render,redirect
from .forms import ContactForm
from django.contrib import messages

# Create your views here.
def index_view(request):
    return render(request,'main/index.html')

#---------------------------------------------------------
def about_view(request):
    return render(request,'main/about.html')
#----------------------------------------------------------
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)  
            obj.name = "Unknown"          
            obj.save()     
            
            messages.success(request, "Your message was sent successfully.")
            return redirect('main:contact')
        else:
            messages.error(request, "Please fix the errors below and try again.")
    else:
        form = ContactForm()
    return render(request,"main/contact.html",{'form':form})