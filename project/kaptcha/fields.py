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


class CaptchaField(forms.CharField):
    widget = CaptchaWidget

    def bound_data(self, data, initial):
        print data, initial
        return data