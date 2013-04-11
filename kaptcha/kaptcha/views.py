from django.shortcuts import render,redirect
from forms import CaptchaForm

def home(request):
    """index.html"""
    form = CaptchaForm(request.POST or None)
    if form.is_valid():
        return redirect('/?s=1')
    return render(request,'index.html',{'form':form})