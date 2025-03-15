from django import forms
from django.contrib.auth import get_user_model
from .models import ChatRoom

User = get_user_model()

class AddUserToChatForm(forms.ModelForm):
    
    user2 = forms.ModelChoiceField(
        queryset=User.objects.none(),  
        label="Select User",
        widget=forms.Select(attrs={'class': 'form-control user-search'})
    )

    class Meta:
        model = ChatRoom
        fields = ['user2']

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)  # Get request from view
        super(AddUserToChatForm, self).__init__(*args, **kwargs)
        if request:
            self.fields['user2'].queryset = User.objects.exclude(id=request.user.id)