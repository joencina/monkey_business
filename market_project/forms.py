from django import forms


class CheckoutForm(forms.Form):
    text_input = forms.TextInput(attrs={'class': 'form-control', 'type': 'text'})
    name = forms.CharField(max_length=200, widget=text_input)
    address = forms.CharField(max_length=200, widget=text_input)
    email_input = forms.EmailInput(attrs={'class': 'form-control', 'type': 'email', 'placeholder': 'example@gmail.com'})
    email = forms.EmailField(max_length=200, widget=email_input)
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your message here'}), required=False)
