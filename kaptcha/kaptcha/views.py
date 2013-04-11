from django.shortcuts import render
from utils import draw_b64_image

from forms import CaptchaForm

def home(request):
    """index.html"""
    form = CaptchaForm({'key':'asdasdasd','captcha':'qweqwrt'})
    return render(request,'index.html',{'form':form})