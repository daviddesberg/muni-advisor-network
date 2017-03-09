from django import forms
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget
from .models import Delegate, PositionPaper, PrintDocument


class RegistrationForm(forms.Form):
    school_name = forms.CharField()
    school_address = forms.CharField(widget=forms.Textarea(attrs={'style': 'height:50px;'}))
    school_phone = PhoneNumberField(widget=PhoneNumberInternationalFallbackWidget)
    initial_advisor_name = forms.CharField(label="Primary advisor name")
    initial_advisor_mobile_phone = PhoneNumberField(widget=PhoneNumberInternationalFallbackWidget,
                                                    label="Primary advisor mobile phone")
    initial_advisor_email = forms.EmailField(label="Primary advisor email")
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

    initial_password = forms.CharField(widget=forms.PasswordInput, min_length=8, label="Password")

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

    country_pref_1 = forms.CharField(label="Insert Country Name", required=False)
    country_pref_2 = forms.CharField(label="Insert Country Name", required=False)
    country_pref_3 = forms.CharField(label="Insert Country Name", required=False)

    additional_notes = forms.CharField(widget=forms.Textarea(attrs={'style': 'height:80px;'}), required=False)


class PositionPaperForm(forms.ModelForm):
    class Meta:
        model = PositionPaper
        fields = ['delegate', 'paper']

    def __init__(self, *args, **kwargs):
        school = kwargs.pop('school', None)
        super(PositionPaperForm, self).__init__(*args, **kwargs)
        self.fields['delegate'].queryset = Delegate.objects.filter(school=school)


class PrintDocumentForm(forms.ModelForm):
    class Meta:
        model = PrintDocument
        fields = ['document', 'committee', 'num_copies', 'comments']
        labels = {
            'num_copies': "Number of copies (please enter a number)"
        }