"""
Tests for the aa_customizer app.

Coverage:
  - CustomBranding model field round-trips (custom CSS/HTML fields)
  - help_text safety — no raw HTML angle-bracket tags that would break the
    Django admin page when rendered via |safe
  - Context processor injects AA_CUSTOMIZER and SITE_NAME
  - Template logic correctly injects custom CSS/HTML into rendered output
  - Template logic suppresses output when fields are blank
"""

from django.db import models as django_models
from django.template import Context, Template
from django.test import RequestFactory, TestCase

from .models import CustomBranding


# ---------------------------------------------------------------------------
# Model round-trip tests
# ---------------------------------------------------------------------------


class CustomCSSFieldsTest(TestCase):
    """CustomBranding fields that hold raw CSS/HTML store and retrieve correctly."""

    def setUp(self):
        self.branding = CustomBranding.get_solo()

    def test_custom_css_round_trip(self):
        css = "body { background: #1a1a2e; } .navbar { color: red; }"
        self.branding.custom_css = css
        self.branding.save()
        self.assertEqual(CustomBranding.get_solo().custom_css, css)

    def test_custom_css_url_round_trip(self):
        url = "https://cdn.example.com/dark-theme.css"
        self.branding.custom_css_url = url
        self.branding.save()
        self.assertEqual(CustomBranding.get_solo().custom_css_url, url)

    def test_head_extra_html_round_trip(self):
        html = '<meta name="description" content="Test site"><script src="analytics.js" defer></script>'
        self.branding.head_extra_html = html
        self.branding.save()
        self.assertEqual(CustomBranding.get_solo().head_extra_html, html)

    def test_login_page_css_url_round_trip(self):
        url = "https://cdn.example.com/login-override.css"
        self.branding.login_page_css_url = url
        self.branding.save()
        self.assertEqual(CustomBranding.get_solo().login_page_css_url, url)

    def test_login_page_css_round_trip(self):
        css = ".card-login { background: rgba(0,0,0,0.9); border-radius: 12px; }"
        self.branding.login_page_css = css
        self.branding.save()
        self.assertEqual(CustomBranding.get_solo().login_page_css, css)

    def test_login_page_head_html_round_trip(self):
        html = '<link rel="preconnect" href="https://fonts.googleapis.com">'
        self.branding.login_page_head_html = html
        self.branding.save()
        self.assertEqual(CustomBranding.get_solo().login_page_head_html, html)

    def test_login_page_body_html_round_trip(self):
        html = '<div id="particle-canvas"></div><script src="particles.min.js"></script>'
        self.branding.login_page_body_html = html
        self.branding.save()
        self.assertEqual(CustomBranding.get_solo().login_page_body_html, html)

    def test_dashboard_css_url_round_trip(self):
        url = "https://cdn.example.com/dashboard-override.css"
        self.branding.dashboard_css_url = url
        self.branding.save()
        self.assertEqual(CustomBranding.get_solo().dashboard_css_url, url)

    def test_dashboard_css_round_trip(self):
        css = ".dashboard-widget { background: #0d0d1a; }"
        self.branding.dashboard_css = css
        self.branding.save()
        self.assertEqual(CustomBranding.get_solo().dashboard_css, css)

    def test_dashboard_head_html_round_trip(self):
        html = '<link rel="preconnect" href="https://fonts.googleapis.com">'
        self.branding.dashboard_head_html = html
        self.branding.save()
        self.assertEqual(CustomBranding.get_solo().dashboard_head_html, html)

    def test_dashboard_body_html_round_trip(self):
        html = '<div id="dash-overlay"></div><script src="widgets.min.js"></script>'
        self.branding.dashboard_body_html = html
        self.branding.save()
        self.assertEqual(CustomBranding.get_solo().dashboard_body_html, html)

    def test_superuser_dashboard_css_url_round_trip(self):
        url = "https://cdn.example.com/admin-panel.css"
        self.branding.superuser_dashboard_css_url = url
        self.branding.save()
        self.assertEqual(CustomBranding.get_solo().superuser_dashboard_css_url, url)

    def test_superuser_dashboard_css_round_trip(self):
        css = ".admin-widget { border: 2px solid red; }"
        self.branding.superuser_dashboard_css = css
        self.branding.save()
        self.assertEqual(CustomBranding.get_solo().superuser_dashboard_css, css)

    def test_superuser_dashboard_head_html_round_trip(self):
        html = '<script src="https://cdn.example.com/chart.js" defer></script>'
        self.branding.superuser_dashboard_head_html = html
        self.branding.save()
        self.assertEqual(CustomBranding.get_solo().superuser_dashboard_head_html, html)

    def test_superuser_dashboard_body_html_round_trip(self):
        html = '<div id="admin-overlay"></div>'
        self.branding.superuser_dashboard_body_html = html
        self.branding.save()
        self.assertEqual(CustomBranding.get_solo().superuser_dashboard_body_html, html)

    def test_all_custom_code_fields_blank_by_default(self):
        for field_name in (
            "custom_css",
            "custom_css_url",
            "head_extra_html",
            "login_page_css_url",
            "login_page_css",
            "login_page_head_html",
            "login_page_body_html",
            "dashboard_css_url",
            "dashboard_css",
            "dashboard_head_html",
            "dashboard_body_html",
            "superuser_dashboard_css_url",
            "superuser_dashboard_css",
            "superuser_dashboard_head_html",
            "superuser_dashboard_body_html",
        ):
            with self.subTest(field=field_name):
                self.assertEqual(getattr(self.branding, field_name), "")


# ---------------------------------------------------------------------------
# help_text safety — guards against admin page parse-break regression
# ---------------------------------------------------------------------------


class HelpTextSafetyTest(TestCase):
    """
    Verify that help_text strings for CSS/HTML fields use HTML entities, not
    raw angle-bracket tags.

    Background: Django admin renders help_text via ``{{ field.field.help_text|safe }}``,
    bypassing all escaping.  A literal ``<style>`` in help_text causes the browser
    to enter CSS-ingestion mode, consuming every subsequent fieldset as CSS text
    — making them invisible in the DOM entirely.

    Fixed in v1.1.16 (commit 7170c15): all raw tags replaced with HTML entities.
    This test prevents regressions.
    """

    FIELDS_TO_CHECK = [
        "custom_css",
        "custom_css_url",
        "head_extra_html",
        "login_page_head_html",
        "login_page_body_html",
        "dashboard_head_html",
        "dashboard_body_html",
        "superuser_dashboard_head_html",
        "superuser_dashboard_body_html",
    ]

    RAW_TAGS_FORBIDDEN = ["<style>", "<head>", "</head>", "</body>"]

    def test_help_text_contains_no_raw_html_tags(self):
        fields_by_name = {
            f.name: f
            for f in CustomBranding._meta.get_fields()
            if isinstance(f, django_models.Field)
        }
        for field_name in self.FIELDS_TO_CHECK:
            field = fields_by_name[field_name]
            help_text = str(field.help_text)
            for raw_tag in self.RAW_TAGS_FORBIDDEN:
                with self.subTest(field=field_name, tag=raw_tag):
                    self.assertNotIn(
                        raw_tag,
                        help_text,
                        f"{field_name}.help_text contains unescaped '{raw_tag}' — "
                        "use HTML entities (&lt;…&gt;) instead to avoid breaking the admin page.",
                    )


# ---------------------------------------------------------------------------
# Context processor
# ---------------------------------------------------------------------------


class ContextProcessorTest(TestCase):
    def test_injects_branding_instance(self):
        from .context_processors import aa_customizer

        ctx = aa_customizer(RequestFactory().get("/"))
        self.assertIn("AA_CUSTOMIZER", ctx)
        self.assertIsInstance(ctx["AA_CUSTOMIZER"], CustomBranding)

    def test_uses_custom_site_name_when_set(self):
        from .context_processors import aa_customizer

        branding = CustomBranding.get_solo()
        branding.site_name = "R3V-W Auth"
        branding.save()
        ctx = aa_customizer(RequestFactory().get("/"))
        self.assertEqual(ctx["SITE_NAME"], "R3V-W Auth")

    def test_falls_back_to_string_site_name_when_blank(self):
        from .context_processors import aa_customizer

        ctx = aa_customizer(RequestFactory().get("/"))
        self.assertIn("SITE_NAME", ctx)
        self.assertIsInstance(ctx["SITE_NAME"], str)


# ---------------------------------------------------------------------------
# Template rendering — mirrors the actual template logic in base-bs5.html and
# public/base.html so we can verify injection without a full AA stack.
# ---------------------------------------------------------------------------


def _render(template_str, context_data):
    return Template(template_str).render(Context(context_data))


class TemplateInjectionTest(TestCase):
    """
    Inline template tests that mirror the exact ``{% if %}``/``|safe`` patterns
    used in the real templates.  Confirms each field ends up in the rendered
    output at the right position.
    """

    def setUp(self):
        self.branding = CustomBranding.get_solo()

    # ── global custom CSS ────────────────────────────────────────────────────

    def test_custom_css_renders_as_inline_style_block(self):
        self.branding.custom_css = "body { background: #0d0d1a; }"
        self.branding.save()
        out = _render(
            "{% if AA_CUSTOMIZER.custom_css %}"
            "<style>{{ AA_CUSTOMIZER.custom_css|safe }}</style>"
            "{% endif %}",
            {"AA_CUSTOMIZER": self.branding},
        )
        self.assertIn("<style>body { background: #0d0d1a; }</style>", out)

    def test_custom_css_url_renders_as_link_tag(self):
        self.branding.custom_css_url = "https://cdn.example.com/dark.css"
        self.branding.save()
        out = _render(
            "{% if AA_CUSTOMIZER.custom_css_url %}"
            '<link rel="stylesheet" href="{{ AA_CUSTOMIZER.custom_css_url }}">'
            "{% endif %}",
            {"AA_CUSTOMIZER": self.branding},
        )
        self.assertIn('href="https://cdn.example.com/dark.css"', out)

    def test_head_extra_html_renders_verbatim(self):
        self.branding.head_extra_html = '<meta name="theme-color" content="#0d0d1a">'
        self.branding.save()
        out = _render(
            "{% if AA_CUSTOMIZER.head_extra_html %}"
            "{{ AA_CUSTOMIZER.head_extra_html|safe }}"
            "{% endif %}",
            {"AA_CUSTOMIZER": self.branding},
        )
        self.assertIn('<meta name="theme-color" content="#0d0d1a">', out)

    # ── login-page-only fields ───────────────────────────────────────────────

    def test_login_page_css_url_renders_as_link_tag(self):
        self.branding.login_page_css_url = "https://cdn.example.com/login.css"
        self.branding.save()
        out = _render(
            "{% if AA_CUSTOMIZER.login_page_css_url %}"
            '<link rel="stylesheet" href="{{ AA_CUSTOMIZER.login_page_css_url }}">'
            "{% endif %}",
            {"AA_CUSTOMIZER": self.branding},
        )
        self.assertIn('href="https://cdn.example.com/login.css"', out)

    def test_login_page_css_renders_as_inline_style_block(self):
        self.branding.login_page_css = ".card-login { background: rgba(0,0,0,0.9); }"
        self.branding.save()
        out = _render(
            "{% if AA_CUSTOMIZER.login_page_css %}"
            "<style>{{ AA_CUSTOMIZER.login_page_css|safe }}</style>"
            "{% endif %}",
            {"AA_CUSTOMIZER": self.branding},
        )
        self.assertIn(
            "<style>.card-login { background: rgba(0,0,0,0.9); }</style>", out
        )

    def test_login_page_head_html_renders_verbatim(self):
        self.branding.login_page_head_html = (
            '<link rel="preconnect" href="https://fonts.googleapis.com">'
        )
        self.branding.save()
        out = _render(
            "{% if AA_CUSTOMIZER.login_page_head_html %}"
            "{{ AA_CUSTOMIZER.login_page_head_html|safe }}"
            "{% endif %}",
            {"AA_CUSTOMIZER": self.branding},
        )
        self.assertIn(
            '<link rel="preconnect" href="https://fonts.googleapis.com">', out
        )

    def test_login_page_body_html_injected_before_body_close(self):
        self.branding.login_page_body_html = '<div id="particles"></div>'
        self.branding.save()
        out = _render(
            "<body>"
            "{% if AA_CUSTOMIZER.login_page_body_html %}"
            "{{ AA_CUSTOMIZER.login_page_body_html|safe }}"
            "{% endif %}"
            "</body>",
            {"AA_CUSTOMIZER": self.branding},
        )
        self.assertIn('<div id="particles"></div></body>', out)

    # ── blank fields produce no output ──────────────────────────────────────

    def test_blank_fields_produce_no_output(self):
        templates = {
            "custom_css": (
                "{% if AA_CUSTOMIZER.custom_css %}"
                "<style>{{ AA_CUSTOMIZER.custom_css|safe }}</style>"
                "{% endif %}"
            ),
            "custom_css_url": (
                "{% if AA_CUSTOMIZER.custom_css_url %}"
                '<link rel="stylesheet" href="{{ AA_CUSTOMIZER.custom_css_url }}">'
                "{% endif %}"
            ),
            "head_extra_html": (
                "{% if AA_CUSTOMIZER.head_extra_html %}"
                "{{ AA_CUSTOMIZER.head_extra_html|safe }}"
                "{% endif %}"
            ),
            "login_page_css": (
                "{% if AA_CUSTOMIZER.login_page_css %}"
                "<style>{{ AA_CUSTOMIZER.login_page_css|safe }}</style>"
                "{% endif %}"
            ),
            "login_page_head_html": (
                "{% if AA_CUSTOMIZER.login_page_head_html %}"
                "{{ AA_CUSTOMIZER.login_page_head_html|safe }}"
                "{% endif %}"
            ),
            "login_page_body_html": (
                "{% if AA_CUSTOMIZER.login_page_body_html %}"
                "{{ AA_CUSTOMIZER.login_page_body_html|safe }}"
                "{% endif %}"
            ),
        }
        for field_name, tpl_str in templates.items():
            with self.subTest(field=field_name):
                out = _render(tpl_str, {"AA_CUSTOMIZER": self.branding})
                self.assertEqual(
                    out.strip(),
                    "",
                    f"Expected no output for blank {field_name}, got: {out!r}",
                )


# ---------------------------------------------------------------------------
# Template rendering — dashboard-specific fields
# ---------------------------------------------------------------------------


class DashboardTemplateInjectionTest(TestCase):
    """
    Tests for main dashboard CSS/HTML injection fields, mirroring the
    ``{% block extra_css %}`` and ``{% block extra_javascript %}`` patterns
    in ``authentication/dashboard.html``.
    """

    def setUp(self):
        self.branding = CustomBranding.get_solo()

    def test_dashboard_css_url_renders_as_link_tag(self):
        self.branding.dashboard_css_url = "https://cdn.example.com/dash.css"
        self.branding.save()
        out = _render(
            "{% if AA_CUSTOMIZER.dashboard_css_url %}"
            '<link rel="stylesheet" href="{{ AA_CUSTOMIZER.dashboard_css_url }}">'
            "{% endif %}",
            {"AA_CUSTOMIZER": self.branding},
        )
        self.assertIn('href="https://cdn.example.com/dash.css"', out)

    def test_dashboard_css_renders_as_inline_style_block(self):
        self.branding.dashboard_css = ".dashboard-widget { background: #0d0d1a; }"
        self.branding.save()
        out = _render(
            "{% if AA_CUSTOMIZER.dashboard_css %}"
            "<style>{{ AA_CUSTOMIZER.dashboard_css|safe }}</style>"
            "{% endif %}",
            {"AA_CUSTOMIZER": self.branding},
        )
        self.assertIn(
            "<style>.dashboard-widget { background: #0d0d1a; }</style>", out
        )

    def test_dashboard_head_html_renders_verbatim(self):
        self.branding.dashboard_head_html = (
            '<link rel="preconnect" href="https://fonts.googleapis.com">'
        )
        self.branding.save()
        out = _render(
            "{% if AA_CUSTOMIZER.dashboard_head_html %}"
            "{{ AA_CUSTOMIZER.dashboard_head_html|safe }}"
            "{% endif %}",
            {"AA_CUSTOMIZER": self.branding},
        )
        self.assertIn(
            '<link rel="preconnect" href="https://fonts.googleapis.com">', out
        )

    def test_dashboard_body_html_renders_verbatim(self):
        self.branding.dashboard_body_html = '<div id="dash-overlay"></div>'
        self.branding.save()
        out = _render(
            "{% if AA_CUSTOMIZER.dashboard_body_html %}"
            "{{ AA_CUSTOMIZER.dashboard_body_html|safe }}"
            "{% endif %}",
            {"AA_CUSTOMIZER": self.branding},
        )
        self.assertIn('<div id="dash-overlay"></div>', out)

    def test_blank_dashboard_fields_produce_no_output(self):
        templates = {
            "dashboard_css_url": (
                "{% if AA_CUSTOMIZER.dashboard_css_url %}"
                '<link rel="stylesheet" href="{{ AA_CUSTOMIZER.dashboard_css_url }}">'
                "{% endif %}"
            ),
            "dashboard_css": (
                "{% if AA_CUSTOMIZER.dashboard_css %}"
                "<style>{{ AA_CUSTOMIZER.dashboard_css|safe }}</style>"
                "{% endif %}"
            ),
            "dashboard_head_html": (
                "{% if AA_CUSTOMIZER.dashboard_head_html %}"
                "{{ AA_CUSTOMIZER.dashboard_head_html|safe }}"
                "{% endif %}"
            ),
            "dashboard_body_html": (
                "{% if AA_CUSTOMIZER.dashboard_body_html %}"
                "{{ AA_CUSTOMIZER.dashboard_body_html|safe }}"
                "{% endif %}"
            ),
        }
        for field_name, tpl_str in templates.items():
            with self.subTest(field=field_name):
                out = _render(tpl_str, {"AA_CUSTOMIZER": self.branding})
                self.assertEqual(
                    out.strip(),
                    "",
                    f"Expected no output for blank {field_name}, got: {out!r}",
                )


# ---------------------------------------------------------------------------
# Template rendering — superuser dashboard fields (via superuser_branding tag)
# ---------------------------------------------------------------------------


class SuperuserDashboardTemplateInjectionTest(TestCase):
    """
    Tests for the superuser admin status widget CSS/HTML injection fields.
    These mirror the patterns in ``allianceauth/admin-status/overview.html``
    which uses the ``{% superuser_branding as aac_sb %}`` simple_tag because
    the inclusion tag that renders overview.html does not pass request context.
    """

    def setUp(self):
        self.branding = CustomBranding.get_solo()

    def _render_with_tag(self, snippet):
        """Render snippet with crum simulating a logged-in superuser."""
        from unittest.mock import MagicMock, patch

        mock_user = MagicMock(is_superuser=True, is_staff=True)
        with patch(
            "aa_customizer.templatetags.aa_customizer_tags.get_current_user",
            return_value=mock_user,
        ):
            return _render(
                "{% load aa_customizer_tags %}"
                "{% superuser_branding as aac_sb %}"
                + snippet,
                {},
            )

    def test_superuser_dashboard_css_url_renders_as_link_tag(self):
        self.branding.superuser_dashboard_css_url = "https://cdn.example.com/admin.css"
        self.branding.save()
        out = self._render_with_tag(
            "{% if aac_sb.superuser_dashboard_css_url %}"
            '<link rel="stylesheet" href="{{ aac_sb.superuser_dashboard_css_url }}">'
            "{% endif %}"
        )
        self.assertIn('href="https://cdn.example.com/admin.css"', out)

    def test_superuser_dashboard_css_renders_as_inline_style_block(self):
        self.branding.superuser_dashboard_css = ".admin-widget { border: 2px solid red; }"
        self.branding.save()
        out = self._render_with_tag(
            "{% if aac_sb.superuser_dashboard_css %}"
            "<style>{{ aac_sb.superuser_dashboard_css|safe }}</style>"
            "{% endif %}"
        )
        self.assertIn(
            "<style>.admin-widget { border: 2px solid red; }</style>", out
        )

    def test_superuser_dashboard_head_html_renders_verbatim(self):
        self.branding.superuser_dashboard_head_html = (
            '<script src="https://cdn.example.com/chart.js" defer></script>'
        )
        self.branding.save()
        out = self._render_with_tag(
            "{% if aac_sb.superuser_dashboard_head_html %}"
            "{{ aac_sb.superuser_dashboard_head_html|safe }}"
            "{% endif %}"
        )
        self.assertIn(
            '<script src="https://cdn.example.com/chart.js" defer></script>', out
        )

    def test_superuser_dashboard_body_html_renders_verbatim(self):
        self.branding.superuser_dashboard_body_html = '<div id="admin-overlay"></div>'
        self.branding.save()
        out = self._render_with_tag(
            "{% if aac_sb.superuser_dashboard_body_html %}"
            "{{ aac_sb.superuser_dashboard_body_html|safe }}"
            "{% endif %}"
        )
        self.assertIn('<div id="admin-overlay"></div>', out)

    def test_superuser_code_suppressed_for_non_superusers(self):
        """
        When crum reports a non-superuser, superuser_branding() returns None
        so every ``{% if aac_sb.xxx %}`` check is falsy and nothing renders.
        """
        from unittest.mock import MagicMock, patch

        self.branding.superuser_dashboard_css = ".secret { color: red; }"
        self.branding.superuser_dashboard_head_html = "<script>alert(1)</script>"
        self.branding.save()

        non_superuser = MagicMock(is_superuser=False, is_staff=False)
        with patch(
            "aa_customizer.templatetags.aa_customizer_tags.get_current_user",
            return_value=non_superuser,
        ):
            output = _render(
                "{% load aa_customizer_tags %}"
                "{% superuser_branding as aac_sb %}"
                "{% if aac_sb.superuser_dashboard_css %}"
                "<style>{{ aac_sb.superuser_dashboard_css|safe }}</style>"
                "{% endif %}"
                "{% if aac_sb.superuser_dashboard_head_html %}"
                "{{ aac_sb.superuser_dashboard_head_html|safe }}"
                "{% endif %}",
                {},
            )

        self.assertEqual(output, "")
        self.assertNotIn(".secret", output)
        self.assertNotIn("alert(1)", output)

    def test_blank_superuser_dashboard_fields_produce_no_output(self):
        templates = {
            "superuser_dashboard_css_url": (
                "{% if aac_sb.superuser_dashboard_css_url %}"
                '<link rel="stylesheet" href="{{ aac_sb.superuser_dashboard_css_url }}">'
                "{% endif %}"
            ),
            "superuser_dashboard_css": (
                "{% if aac_sb.superuser_dashboard_css %}"
                "<style>{{ aac_sb.superuser_dashboard_css|safe }}</style>"
                "{% endif %}"
            ),
            "superuser_dashboard_head_html": (
                "{% if aac_sb.superuser_dashboard_head_html %}"
                "{{ aac_sb.superuser_dashboard_head_html|safe }}"
                "{% endif %}"
            ),
            "superuser_dashboard_body_html": (
                "{% if aac_sb.superuser_dashboard_body_html %}"
                "{{ aac_sb.superuser_dashboard_body_html|safe }}"
                "{% endif %}"
            ),
        }
        for field_name, tpl_str in templates.items():
            with self.subTest(field=field_name):
                out = self._render_with_tag(tpl_str)
                self.assertEqual(
                    out.strip(),
                    "",
                    f"Expected no output for blank {field_name}, got: {out!r}",
                )


# ---------------------------------------------------------------------------
# Trusted-user admin restriction (AA_CUSTOMIZER_TRUSTED_USER_IDS)
# ---------------------------------------------------------------------------


class TrustedAdminUserTests(TestCase):
    """
    Tests for the AA_CUSTOMIZER_TRUSTED_USER_IDS admin access restriction.

    When the setting is absent or empty, any superuser passes.
    When the setting is a non-empty list, only users whose pk appears in that
    list are allowed — regardless of superuser flag.
    """

    def _make_request(self, pk, is_superuser=True):
        request = RequestFactory().get("/")
        from unittest.mock import MagicMock
        request.user = MagicMock(pk=pk, is_superuser=is_superuser, is_staff=is_superuser)
        return request

    def test_no_setting_allows_superuser(self):
        """Without the setting, any superuser is trusted."""
        from .permissions import _is_trusted_admin
        with self.settings(AA_CUSTOMIZER_TRUSTED_USER_IDS=[]):
            self.assertTrue(_is_trusted_admin(self._make_request(pk=42, is_superuser=True)))

    def test_no_setting_blocks_non_superuser(self):
        """Without the setting, non-superusers are blocked."""
        from .permissions import _is_trusted_admin
        with self.settings(AA_CUSTOMIZER_TRUSTED_USER_IDS=[]):
            self.assertFalse(_is_trusted_admin(self._make_request(pk=42, is_superuser=False)))

    def test_trusted_list_allows_listed_pk(self):
        """A user whose PK appears in the trusted list is allowed."""
        from .permissions import _is_trusted_admin
        with self.settings(AA_CUSTOMIZER_TRUSTED_USER_IDS=[1, 7]):
            self.assertTrue(_is_trusted_admin(self._make_request(pk=7)))

    def test_trusted_list_blocks_unlisted_superuser(self):
        """A superuser whose PK is NOT in the trusted list is blocked."""
        from .permissions import _is_trusted_admin
        with self.settings(AA_CUSTOMIZER_TRUSTED_USER_IDS=[1, 7]):
            self.assertFalse(_is_trusted_admin(self._make_request(pk=99, is_superuser=True)))

    def test_trusted_list_allows_by_pk_regardless_of_superuser_flag(self):
        """_is_trusted_admin gates on PK membership alone when the list is set."""
        from .permissions import _is_trusted_admin
        with self.settings(AA_CUSTOMIZER_TRUSTED_USER_IDS=[5]):
            # pk=5 is in list; is_superuser flag is irrelevant when list is active
            self.assertTrue(_is_trusted_admin(self._make_request(pk=5, is_superuser=False)))

    def test_trusted_list_with_single_entry(self):
        """Edge case: a single-element list still enforces the restriction correctly."""
        from .permissions import _is_trusted_admin
        with self.settings(AA_CUSTOMIZER_TRUSTED_USER_IDS=[3]):
            self.assertTrue(_is_trusted_admin(self._make_request(pk=3)))
            self.assertFalse(_is_trusted_admin(self._make_request(pk=4)))
