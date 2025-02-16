from django import forms
from .models import Project , ProjectPost


account_choices = (
    ('hunter' ,'Hunter') ,
    ('company' , 'Company')

)


class AccountTypeForm(forms.Form):
    account_type = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=account_choices,
        required=True, 
        label="Select Account Type",
    )

class CreateProjectForm(forms.ModelForm):
    class Meta:
        model=Project
        fields=('name' , 'description' , 'website')


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = ProjectPost
        fields =['image','text' , 'post_type']
