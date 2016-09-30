from django import forms
from phonenumber_field.formfields import PhoneNumberField


class RegistrationForm(forms.Form):
    school_name = forms.CharField()
    school_address = forms.CharField(widget=forms.Textarea(attrs={'style': 'height:50px;'}))
    school_phone = PhoneNumberField()
    initial_advisor_name = forms.CharField()
    initial_advisor_email = forms.EmailField()
    rough_number_of_delegates = forms.IntegerField()

    transportation_required = forms.TypedChoiceField(
        label="Will your delegation require transportation during the conference?",
        choices=(
            (1, 'Yes'),
            (0, 'No')
        ),
        widget=forms.RadioSelect,
        coerce=int
    )

    initial_password = forms.CharField(widget=forms.PasswordInput)

    crisis_interested = forms.TypedChoiceField(
        label="Is your delegation interested in Crisis Committees?",
        choices=(
            (1, 'Yes, our delegation is interested in Crisis Committees'),
            (0, 'No, our delegation is not interested in Crisis Committees')
        ),
        widget=forms.RadioSelect,
        coerce=int
    )

    ipd_position_interested = forms.TypedChoiceField(
        label="Is your delegation interested in International Press Delegation (IPD) positions?",
        choices=(
            (1, 'Yes, our delegation is interested in IPD positions'),
            (0, 'No, our delegation is not interested in IPD positions')
        ),
        widget=forms.RadioSelect,
        coerce=int
    )

    country_pref_1 = forms.CharField(label="Insert Country Name")
    country_pref_2 = forms.CharField(label="Insert Country Name")
    country_pref_3 = forms.CharField(label="Insert Country Name")

    additional_notes = forms.CharField(widget=forms.Textarea(attrs={'style': 'height:80px;'}))
