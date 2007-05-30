"""
Form and validation code for user registration.

"""
from django.contrib.auth.models import User

import sys
sys.path.append("./registration/svn_newforms")
import newforms as forms
import fields, widgets

# I put this on all required fields, because it's easier to pick up
# on them with CSS or JavaScript if they have a class of "required"
# in the HTML. Your mileage may vary.
attrs_dict = { 'class': 'required' }

class RegistrationForm(forms.Form):
    """
    Form for registering a new user account.
    
    Validates that the password is entered twice and matches,
    and that the username is not already taken.
    
    """
    username = fields.CharField(max_length=30,
                               widget=widgets.TextInput(attrs=attrs_dict),
                               label=u'Username')
    email = fields.EmailField(widget=widgets.TextInput(attrs=dict(attrs_dict,
                                                               maxlength=200)),
                             label=u'Email address')
    password1 = fields.CharField(widget=widgets.PasswordInput(attrs=attrs_dict),
                                label=u'Password')
    password2 = fields.CharField(widget=widgets.PasswordInput(attrs=attrs_dict),
                                label=u'Password (again, to catch typos)')

    def clean_username(self):
        """
        Validates that the username is not already in use.
        
        """
        if self.clean_data.get('username', None):
            try:
                user = User.objects.get(username__exact=self.clean_data['username'])
            except User.DoesNotExist:
                return self.clean_data['username']
            raise forms.ValidationError(u'The username "%s" is already taken. Please choose another.' % self.clean_data['username'])
    
    def clean_password2(self):
        """
        Validates that the two password inputs match.
        
        """
        if self.clean_data.get('password1', None) and self.clean_data.get('password2', None) and \
           self.clean_data['password1'] == self.clean_data['password2']:
            return self.clean_data['password2']
        raise forms.ValidationError(u'You must type the same password each time')
    
