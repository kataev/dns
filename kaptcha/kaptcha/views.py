from django.shortcuts import render
import redis
from forms import CaptchaForm

def home(request):
    """index.html"""
    form = CaptchaForm({'text':'asd','key':'asdasdasd','captcha':'qweqwrt'})
    r = redis.Redis()
    r.sadd('capcha','asdasd')
    print r.sismember('capcha','asdasd')
    return render(request,'index.html',{'form':form})