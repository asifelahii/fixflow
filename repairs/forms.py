from django import forms


class TrackingForm(forms.Form):
    tracking_code = forms.CharField(
        max_length=16,
        label="Tracking code",
        strip=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "e.g. K2E362D5MW31",
                "autocomplete": "off",
                "autocapitalize": "characters",
                "spellcheck": "false",
                "aria-describedby": "tracking-help",
            }
        ),
    )

    def clean_tracking_code(self):
        tracking_code = self.cleaned_data["tracking_code"]

        return tracking_code.strip().upper()