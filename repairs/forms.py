from django import forms


class TrackingForm(forms.Form):
    tracking_code = forms.CharField(
        max_length=16,
        label="Tracking code",
        strip=True,
    )

    def clean_tracking_code(self):
        tracking_code = self.cleaned_data["tracking_code"]

        return tracking_code.strip().upper()