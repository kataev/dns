import random
import redis
import binascii

from utils import draw_b64_image

from django import forms

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
        image = draw_b64_image(self.text)
        img = '<img src="data:image/png;base64,{}" style="display:block;clear:both;">'.format(image)
        return format_html(img + '<input{0} />', flatatt(final_attrs))


captcha = redis.Redis()

def get_key():
    return ''.join(random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(20))

def get_hash(key):
    return str(binascii.crc32(key))[-6:]


class CaptchaForm(forms.Form):
    def __init__(self, data, *args, **kwargs):
        initial = kwargs.get('initial') or {}
        key = get_key()
        hash = get_hash(key)
        initial['key'] = key
        kwargs['initial'] = initial
        super(CaptchaForm, self).__init__(data, *args, **kwargs)
        self.fields['captcha'].widget.text = hash

    text = forms.CharField()
    key = forms.CharField()#widget=forms.HiddenInput)
    captcha = forms.CharField(widget=CaptchaWidget(attrs={'autocomplete': 'off'}))

    def clean(self):
        cleaned_data = super(CaptchaForm, self).clean()

        key = cleaned_data.pop('key')
        chash = cleaned_data.pop('captcha')

        if captcha.sismember('used', key):
            raise forms.ValidationError('Captcha fail: alredy used')

        shash = get_hash(key)
        if chash != shash:
            key = get_key() # get new key and hash for new attempt
            shash = get_hash(key)
            self.fields['captcha'].widget.text = shash
            self.data = dict(key=key,**cleaned_data)
            raise forms.ValidationError('Captcha compare failed!')
        else:
            captcha.sadd('used', key)
        return cleaned_data