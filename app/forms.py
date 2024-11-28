"""Forms for the app."""

from allauth.account.forms import SignupForm
from django import forms


class CreateArticleForm(forms.Form):
    """Form for creating an Article."""

    ARTICLE_STATUS = (("draft", "draft"), ("inprogress", "in progress"), ("published", "published"))

    title = forms.CharField(max_length=100)
    content = forms.CharField(widget=forms.Textarea)
    word_count = forms.IntegerField()
    twitter_post = forms.CharField(widget=forms.Textarea, required=False)
    status = forms.ChoiceField(choices=ARTICLE_STATUS)

class CustomSignupForm(SignupForm):
    """Custom form for creating a user. Includes first and last name."""

    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    def save(self, request):
        """Save the user and update their first and last name."""
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.save()
        return user

