"""
Forms for the aa_customizer app.
"""

from django import forms

from .models import CustomBranding, _ALLOWED_BACKGROUND_EXTENSIONS

_MONO = "font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace; width: 100%;"

# Characters that are dangerous inside a raw CSS property value context.
# The login_background_color field is interpolated as:
#   background: <value>;
# inside a <style> block.  A } closes the rule and allows injecting arbitrary
# CSS selectors; ; allows injecting extra properties before the closing }.
_CSS_INJECTION_CHARS = frozenset("{}\\<>")


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
            "login_page_css": forms.Textarea(attrs={"rows": 14, "style": _MONO}),
            "login_page_head_html": forms.Textarea(attrs={"rows": 8, "style": _MONO}),
            "login_page_body_html": forms.Textarea(attrs={"rows": 8, "style": _MONO}),
        }

    def clean_login_background_color(self):
        value = self.cleaned_data.get("login_background_color", "")
        bad = _CSS_INJECTION_CHARS & set(value)
        if bad:
            raise forms.ValidationError(
                "Invalid color value — the following characters are not allowed: "
                + ", ".join(sorted(bad))
                + ". Use a valid CSS color such as #1a1a2e or rgba(26, 26, 46, 1)."
            )
        return value

    def clean_login_background(self):
        f = self.cleaned_data.get("login_background")
        if f and hasattr(f, "name"):
            import os
            ext = os.path.splitext(f.name)[1].lower()
            if ext not in _ALLOWED_BACKGROUND_EXTENSIONS:
                raise forms.ValidationError(
                    f"Unsupported file type '{ext}'. "
                    "Please upload an image (JPEG, PNG, GIF, WebP) or a video (MP4, WebM, OGV)."
                )
        return f
