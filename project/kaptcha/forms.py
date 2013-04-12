import os
import random
import redis
from binascii import crc32
from hashlib import sha256

from django import forms

from fields import CaptchaField


redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
captcha = redis.from_url(redis_url)


def get_key(length=20):
    return ''.join(
        random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(length))


salt = get_key(40)


def get_hash(key):
    return str(crc32(sha256(sha256(key).hexdigest() + salt).hexdigest()))[-6:]


class CaptchaForm(forms.Form):
    def __init__(self, data=None, *args, **kwargs):
        initial = kwargs.get('initial') or {}
        key = get_key()
        hash = get_hash(key)
        initial['key'] = key
        kwargs['initial'] = initial
        super(CaptchaForm, self).__init__(data, *args, **kwargs)
        self.fields['captcha'].widget.text = hash

    text = forms.CharField()
    key = forms.CharField(widget=forms.HiddenInput)
    captcha = CaptchaField()

    def clean(self):
        cleaned_data = super(CaptchaForm, self).clean()
        key = cleaned_data.pop('key', '')
        chash = cleaned_data.pop('captcha', '')
        if not self.errors:
            if captcha.sismember('used', key):
                raise forms.ValidationError('Captcha fail: alredy used')
            shash = get_hash(key)
            if chash != shash:
                key = get_key() # get new key and hash for new attempt
                shash = get_hash(key)
                self.fields['captcha'].widget.text = shash
                self.data = dict(key=key, **cleaned_data)
                raise forms.ValidationError('Captcha compare failed!')
            else:
                captcha.sadd('used', key)
        return cleaned_data