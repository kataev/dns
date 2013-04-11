from django import forms
from utils import draw_b64_image

from django.utils.encoding import force_text
from django.utils.html import format_html
from django.forms.util import flatatt

class CaptchaWidget(forms.TextInput):
    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_text(self._format_value(value))
        image = draw_b64_image(value)
        img = '<img src="data:image/png;base64,{}"></img>'.format(image)
        print 'text'
        return format_html(img+'<input{0} />', flatatt(final_attrs))


class CaptchaForm(forms.Form):
    key = forms.CharField()
    captcha = forms.CharField(widget=CaptchaWidget)