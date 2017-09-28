from django import forms
from django.core.exceptions import ValidationError
# from activity.models import Chat


class ChatForm(forms.ModelForm):
    title = 'Chat with me'
    
    class Meta:
        comment = Chat
        fields = ['username', 'message']
        error_messages = {'required': 'This field is required'}

    def clean(self):
        if self.cleaned_data.get('message') <= 0:
            raise ValidationError("Write wour message.")
        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super(ChatForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
            # self.fields['name'].widget.attrs['placeholder'] = 'User'
            self.fields['message'].widget.attrs['placeholder'] = 'Comments'
