from django.shortcuts import render
import base64
from utils import draw_captcha
import StringIO

from forms import KaptchaForm

def home(request):
    """index.html"""
    form = KaptchaForm()
    image = draw_captcha('text')
    output = StringIO.StringIO()
    image.save(output, format='PNG')
    content = base64.b64encode(output.getvalue())
    output.close()

    # content = 'iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAYlJREFUeNrMVD1rwlAUPfkwBBxFKQQlDhmjqzj4F9w7FfwThZaW9n8UnDrrn1BEXNTBRQQhEE1ERRR0Sd990A7VaKJJ6YHzEu4N99z3zrsRGo2GAuCF8YFRQzSwGOuM7zJb3hgfES2o0SdGSWRLDfGhRgLpGAXS4q0VCoUCBEHwzd8skM/nUSqVoCjKybz8O1CtVn2LeZ4H27YxnU6xXC6x3+95PJPJoFKpoN1uY7vdnhfww3w+x3A4xGaz4d3quo5sNvuTTyaTXKTb7cJ13csCzWbzKKaqKj/zXC4HSZKO8iRcLpcxGAwwmUzC7UDTNBSLRSQSiVAeyUGNpM4v4XA4oNfr8eMMLJBKpWCaJn9fLBawLAur1Qq73Y6b/H0pyNyrTDYMA7PZDKPRCOv1+uQ3ZCqZe9UcOI6DTqfjW5zMbLVa3Bu6RaE9GI/HZ/P9fp8/qfipYROj+ukEnuQgEx0GImKGHGSC//UO/kTAibG+QwIfMQrUyeRXusaM94x3ERW2GT8Zn78EGACRmoKUJhB1TQAAAABJRU5ErkJggg=='
    return render(request,'index.html',{'form':form,'img':content})