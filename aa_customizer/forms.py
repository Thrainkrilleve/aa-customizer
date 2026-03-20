"""
Forms for the aa_customizer app.
"""

from django import forms

from .models import CustomBranding

_MONO = "font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace; width: 100%;"


class CustomBrandingAdminForm(forms.ModelForm):
    """Form for the CustomBranding admin."""

    class Meta:
        model = CustomBranding
        fields = "__all__"
        widgets = {
            "login_subtitle": forms.Textarea(attrs={"rows": 3}),
            "custom_css": forms.Textarea(attrs={"rows": 14, "style": _MONO}),
            "login_extra_html": forms.Textarea(attrs={"rows": 6, "style": _MONO}),
            "head_extra_html": forms.Textarea(attrs={"rows": 6, "style": _MONO}),
        }
