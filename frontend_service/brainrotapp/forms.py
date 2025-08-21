from django import forms

class PromptForm(forms.Form):
    PROMPT_RATIOS = [
        ('1:1', '1:1'),
        ('4:3', '4:3'),
        ('16:9', '16:9'),
    ]
    
    prompt_input = forms.CharField(
        label='Prompt',
        max_length=100,
        widget=forms.TextInput(attrs={
            'id': 'prompt_input',
            'placeholder': 'Введите prompt'
        })
    )
    
    image_ratio = forms.ChoiceField(
        choices=PROMPT_RATIOS,
        initial='4:3',
        widget=forms.Select(attrs={'id': 'image_ratio'})
    )


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"id": "login_input"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"id": "password_input"}))