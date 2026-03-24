# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.4] - 2026-03-23
### Fixed
- **SPA mode ignores split layout setting** — when Login Page SPA mode was enabled, the `aac-split` / `aac-split-right` layout classes were still applied to `.aac-login-root`. When a visitor clicked "Sign In" and the SPA overlay dismissed, the login card appeared as a full split-screen layout instead of a centred card. The split classes are now suppressed when SPA mode is active.

## [1.2.3] - 2026-03-23
### Fixed
- **SPA template comments rendering as text** — `{# ... #}` Django shorthand comments in `base.html` and `login_spa_shell.html` were leaking through as visible text on the login page in some server environments. The inline comment in `base.html` has been removed and the docstring block in `login_spa_shell.html` has been converted to `{% comment %}...{% endcomment %}`, which is a proper template node that is always stripped regardless of how the template loader processes the file.

## [1.2.2] - 2026-03-23
### Fixed
- **SPA content bleeding through** — when `login_spa_enabled` is True, `login_page_body_html` is now wrapped in a hidden container before being injected into the DOM. The SPA JavaScript reads content from it normally via `getElementById`/`querySelector`, but any old-format HTML (without the `#aac-spa-content` wrapper) can no longer bleed through and render visibly on the page. `#aac-spa-body-src` and `#aac-spa-content` are also locked with `display: none !important` in the SPA CSS as a belt-and-suspenders measure.
- **Migration 0018** — captures `help_text` updates on `login_page_body_html` (added SPA usage guidance) and `login_spa_enabled` (expanded instructions) that were missed in earlier migrations.
### Removed
- `custom.css` and `customindex.html` — instance-specific development files removed from the repository.

## [1.2.1] - 2026-03-23
### Fixed
- **Media Library access restriction** — `AACMediaImageAdmin` was missing all permission overrides, allowing any superuser to access the Media Library even when `AA_CUSTOMIZER_TRUSTED_USER_IDS` was configured. All four permission methods (`has_view`, `has_add`, `has_change`, `has_delete`) now delegate to `_is_trusted_admin()`, matching `CustomBrandingAdmin`. Nine new tests verify the restriction at every level, including admin index visibility.

## [1.2.0] - 2026-03-23
### Added
- **Login Page SPA mode** — new `login_spa_enabled` toggle and `login_spa_nav_brand` field in Custom Branding admin. When enabled, a full-viewport overlay SPA is rendered on the login page. Admins define page content via the existing *Extra Body HTML* field using `<div id="aac-spa-content">` containing `<section data-route="slug" data-label="Nav Label">` elements. The JS router reads these at load time, builds nav links automatically, and handles hash-based routing. Navigating to `#signin` (or arriving with a `?next=` query param) hides the overlay and reveals the standard EVE SSO login card. Bundled CSS (`aac-spa-*` class prefix) is served automatically as a static file when SPA mode is on; each class is namespaced to avoid collisions with Bootstrap or Alliance Auth. Nav brand text defaults to `SITE_NAME` when left blank. See `login-spa.html` for a copy-paste scaffold.

## [1.1.27] - 2026-03-23
### Added
- **`AA_CUSTOMIZER_TRUSTED_USER_IDS` setting** — optional list of integer user PKs in `local.py` that restricts access to the CustomBranding admin page. When set, only the listed users may view or modify branding settings, regardless of superuser status. When absent or empty, any superuser retains access (backward-compatible). The permission helper lives in `aa_customizer/permissions.py` so it can be tested without requiring `django.contrib.admin` in `INSTALLED_APPS`.

## [1.1.26] - 2026-03-23
### Fixed
- **`celery_bar_partial.html` override removed** — the override's `|default:"0"` guards returned `SafeString("0")` when `tasks_count` was `None` or `0`, causing `decimal_widthratio` to crash with `TypeError: unsupported operand type(s) for /: 'SafeString' and 'int'` and breaking the entire dashboard. The stock AA template works correctly because the view always provides integer values; the override was unnecessary and harmful.

## [1.1.25] - 2026-03-23
### Fixed
- **`pyproject.toml` package-data** — added `templates/allianceauth/**/*.html` and `templates/authentication/*.html` glob patterns. Without these, pip installations were missing the `authentication/dashboard.html` override (so `superuser_dashboard_*` fields never rendered) and the `allianceauth/admin-status/` template overrides (`overview.html`, `celery_bar_partial.html`, `esi_check.html`). All template overrides now ship correctly in the installed package.

## [1.1.24] - 2026-03-23
### Fixed
- **`authentication/dashboard.html`** — added `{{ block.super }}` and rendered all `superuser_dashboard_*` fields; moved `superuser_dashboard_body_html` into `{% block content %}` above the dashboard panels.

## [1.1.23] - 2026-03-23

### Fixed
- **Template override priority** — `AppConfig.ready()` now appends `aa_customizer/templates/` to `settings.TEMPLATES[*]['DIRS']` at startup. This is required because Alliance Auth mandates `'allianceauth'` be first in `INSTALLED_APPS` (for Django admin favicon support), which causes Django's `app_directories` loader to find `allianceauth`'s own templates *before* ours. By inserting into the `DIRS` filesystem loader chain (which runs before `APP_DIRS`), all of our template overrides (`allianceauth/base-bs5.html`, `allianceauth/admin-status/overview.html`, `authentication/dashboard.html`, etc.) now correctly take effect. User project-level `DIRS[0]` entries still retain the highest priority.
- **`superuser_branding` tag uses `crum.get_current_user()`** — the `{% status_overview %}` inclusion tag in AA does not pass `takes_context=True`, so `request` is never forwarded to `overview.html`. The tag now reads the active user from crum's thread-local storage instead of the template context, fixing all cases where the tag returned `None` for a legitimate superuser.
- **`dashboard.html` `{{ block.super }}`** — the `{% block extra_css %}` override now calls `{{ block.super }}` before injecting customizer styles, preserving any CSS blocks that parent templates or other apps have already registered.

## [1.1.22] - 2026-03-22

### Added
- **`get_branding` template tag** — generic alias for `superuser_branding` usable from any third-party plugin template that lacks the context processor output.
- **`aac-dashboard-context` CSS hook** — the dashboard row div now carries this class, giving users a stable specificity anchor (`.aac-dashboard-context .card { … }`) without needing `!important`.

### Changed
- **Admin fieldsets reorganized** — `CustomBrandingAdmin` collapsed from 12 granular fieldsets into 6 logical sections. All four "Custom Code" sections start collapsed by default, so the visual branding fields are immediately visible without scrolling past textarea fields.
- **`forms.py` monospace widgets** — the six dashboard code fields (`dashboard_css`, `dashboard_head_html`, `dashboard_body_html`, `superuser_dashboard_css`, `superuser_dashboard_head_html`, `superuser_dashboard_body_html`) now render with the shared monospace `Textarea` style, consistent with all other code fields.
- **`overview.html` template polish** — mobile stacking gap (`mb-3 mb-xl-0`) on the software-version column; version card headings downgraded to `<h6>` and centred; `{% blocktranslate %}` spans pre-populated with server-side `{{ total }}`/`{{ latest }}` values; progress bar height reduced from 21 px to 12 px; task count spans pre-populated from `tasks_succeeded`, `tasks_retried`, and `tasks_failed` context variables so the initial render shows real data before the first 30-second poll.
- **`celery_bar_partial.html` override** — new template override adds `|default:"0"` guards on `tasks_count` and `tasks_total`, and a `{% if safe_total %}` zero-division guard so the progress bar never crashes on a cold start.
- **`esi_check.html` override** — jQuery `$(document).ready()` replaced with vanilla `DOMContentLoaded`; added `fetchGet` existence guard with a `console.warn` fallback; `data.error` now type-checked with an `"Unknown error occurred."` fallback string; `.catch()` surfaces the error in the UI instead of swallowing it; `bootstrap.Collapse` call guarded with a `classList.remove('collapse')` fallback; container gains `aria-live="polite"`; `<pre>` block gains `max-height: 300px; overflow-y: auto`; status message uses `{% blocktranslate %}` for correct i18n word order.

### Tests
- Added `test_superuser_code_suppressed_for_non_superusers` — confirms the AA view gate prevents custom superuser code from reaching non-superuser responses. Total: 39 tests.

## [1.1.21] - 2026-03-23

### Added
- **Per-section CSS/HTML customization** — the admin panel now has two additional "Custom Code" fieldsets for targeting specific sections of the authenticated site:
  - **Main Dashboard — Custom Code** (`dashboard_css_url`, `dashboard_css`, `dashboard_head_html`, `dashboard_body_html`) — styles and markup applied only on the post-login dashboard page, via a template override of `authentication/dashboard.html` that injects into `{% block extra_css %}` (for head assets) and `{% block extra_javascript %}` (for body scripts/markup).
  - **Admin Dashboard — Custom Code** (`superuser_dashboard_css_url`, `superuser_dashboard_css`, `superuser_dashboard_head_html`, `superuser_dashboard_body_html`) — styles and markup injected into the superuser status widget (`allianceauth/admin-status/overview.html`). These are **superuser-only**: non-superusers never see the widget and therefore never receive these styles. Uses a new `{% superuser_branding %}` template tag to access `CustomBranding.get_solo()` directly because the AA `{% status_overview %}` inclusion tag does not forward request context.
- **`superuser_branding` template tag** — new `simple_tag` in `aa_customizer_tags.py` that returns the `CustomBranding` singleton directly from the DB (django-solo cached). Usable in any template that does not receive the context processor output.
- **Migration `0016`** — adds the 8 new `URLField`/`TextField` columns to `custombranding`.
- **Unit tests** — 18 new tests (38 total): 8 model round-trip tests for the new fields, updated `test_all_custom_code_fields_blank_by_default` covering all 15 text/URL fields, expanded `HelpTextSafetyTest` checking 9 fields for raw-tag regressions, `DashboardTemplateInjectionTest` (5 cases), and `SuperuserDashboardTemplateInjectionTest` (5 cases).

## [1.1.20] - 2026-03-22

### Fixed
- **Language selector clipped on login card** — Alliance Auth’s `lang_select.html` wraps the language `<select>` in a `<form class="dropdown-item">`, which applies Bootstrap’s `white-space: nowrap` and causes the option text (e.g. “English (en)”) to be cut off inside the login card. Added a template override at `public/lang_select.html` that replaces the `dropdown-item` class with `px-3 py-2` spacing and uses `form-select-sm` for a neater fit.

## [1.1.19] - 2026-03-22

### Fixed
- **Migration** — added migration `0015` for the `help_text` changes on seven fields introduced in v1.1.18 (`custom_css`, `custom_css_url`, `head_extra_html`, `login_page_body_html`, `login_page_css`, `login_page_css_url`, `login_page_head_html`). Django's system check was failing with "Unmigrated model changes detected" in CI.

## [1.1.18] - 2026-03-22

### Changed
- **Admin panel cleanup** — merged the separate "Custom CSS" and "Extra HTML" fieldsets into a single "Site-Wide CSS & HTML" section. Moved "Login Page — Custom Code" up to sit next to the other login-page sections. Trimmed redundant `help_text` on six fields whose descriptions were already covered by the fieldset header.
- **CCP attribution footer** — added a `.aac-ccp-footer` attribution block to `customindex.html` and `docs/showcase.html` footers with EVE SSO / ESI credit, CCP Developers link, Privacy link, and repo attribution. All footer styling moved to CSS classes in `custom.css` (`#aac-footer > a` hover rules + `.aac-ccp-footer` block/link/hover rules); no inline styles remain.
- **README** — merged "Custom CSS" and "Extra HTML" field-reference sections into "Site-Wide CSS & HTML" to match the updated admin panel.

## [1.1.17] - 2026-03-22

### Added
- **Login page showcase** — added `custom.css` and `customindex.html` reference files demonstrating a complete EVE Online corporation landing-page redesign using only the four login-page custom-code fields, with no server-side changes required.
- **Interactive docs** — new **Login Showcase** section in the documentation site (`docs/index.html`) with a live embedded `<iframe>` demo, field-by-field attribution cards, and a "How the modal works" explanation box.
- **Standalone showcase demo** — `docs/showcase.html` self-contained demo page: corp landing page with scroll-reveal, count-up stats, feature cards, CTA, and the Alliance Auth login card as a modal overlay.
- **Unit tests** — 20 unit tests covering context processors, custom code field round-trips, help-text safety, and template injection for all eight custom HTML/CSS fields (`aa_customizer/tests.py`).

### Fixed
- **Type annotations** — `effective_*` property helpers in `models.py` now use a local variable (`lib = self.xxx_library`) pattern for FK access instead of the Django-generated `_id` attribute, resolving all Pyright `reportAttributeAccessIssue` errors. `CustomBranding.Meta` annotated with `# type: ignore[override]` to suppress the false-positive `reportIncompatibleVariableOverride` from Pyright's incomplete solo stubs.

### Changed
- **README** — features table updated with four login-page custom-code field rows: Login Page CSS URL, Login Page CSS (Inline), Login Page Extra `<head>` HTML, Login Page Extra Body HTML.
- **Docs** — interactive site version badge updated to v1.1.17.

## [1.1.16] - 2026-03-22

### Fixed
- **Admin** — five `help_text` strings on custom code fields (`login_page_css_url`, `login_page_css`, `login_page_head_html`, `login_page_body_html`, and `custom_css_url`) contained literal `<style>`, `<head>`, and `</body>` HTML tags. Django was parsing these tags as real HTML inside the admin fieldset, causing the entire fieldset to collapse and hide all fields within it. Replaced with HTML entities (`&lt;style&gt;`, `&lt;head&gt;`, `&lt;/body&gt;`) so the help text renders as plain readable text. Migration `0014` applied.

## [1.1.15] - 2026-03-22

### Fixed
- **Admin** — login page custom code fields (`login_page_css_url`, `login_page_css`, `login_page_head_html`, `login_page_body_html`) were missing from the admin fieldsets and therefore invisible in the Django admin panel. Added "Login Page — Custom Code" fieldset to expose all four fields.

## [1.1.4] - 2026-03-22

### Changed
- **Docs** — updated field reference and feature cards for v1.1.3 features; corrected Docker installation note (bind mount, not named volume).

## [1.1.3] - 2026-03-22

### Added
- **Login page video upload** — `login_background` field changed from `ImageField` to `FileField` with a validator allowing standard image formats (JPEG, PNG, GIF, WebP) and web video formats (MP4, WebM, OGV). Admins can now upload video files directly without needing an external URL (migration `0012`).
- **Login page custom code** — four new fields for a fully custom login page design: `Login Page — CSS URL`, `Login Page — CSS`, `Login Page — Extra <head> HTML`, and `Login Page — Extra Body HTML`. These fields are scoped exclusively to the login page, injected after all global styles for maximum override power (migration `0013`).

## [1.1.2a] - 2026-03-22

### Changed
- **Interactive documentation site** — synced field reference with README: moved Login Page Extra HTML to the Login Branding section, added separate Login Logo image recommendation card, added Background Video — Loop Count row, and updated video background descriptions to mention configurable loop count.
- **README** — added Background Video — Loop Count to the field reference table and updated the features table and Login Background URL description to mention configurable loop count.
- **Overview page** — added current version badge.

## [1.1.2] - 2026-03-22

### Added
- **Background video loop count** — new `Background Video — Loop Count` field in the admin panel. Set to `0` (default) to loop forever, `1` to play once and freeze on the last frame, or `N` to play exactly N times then freeze. Implemented via a `PositiveSmallIntegerField` on `CustomBranding` (migration `0011`).

### Changed
- **Interactive documentation site** — added `docs/index.html`, a self-contained interactive docs page (Tailwind CSS + Chart.js) covering the installation guide, field reference, media strategy, and security notes. Enabled as a GitHub Pages site at `https://thrainkrilleve.github.io/aa-customizer/`.
- **README** — added link to the interactive documentation site.

## [1.1.1] - 2026-03-21

### Fixed
- **Django 6.0 field serialization for 0009 fields** — Django 6.0 re-serializes `CharField`, `URLField`, and `ForeignKey` definitions differently from earlier versions, causing `MigrationAutodetector` to detect false-positive changes on fields introduced in migration 0009. Added `0010_alter_fields_django6_compat` to align the recorded state with Django 6.0's output.

## [1.1.0] - 2026-03-21

### Added
- **Media Library** — a new `AA Customizer → Media Library` section in the admin lets you upload and name images once, then reuse them across any image slot without re-uploading. Each image slot (login background, login logo, favicon, navbar logo, sidebar logo) now has a **Library** dropdown alongside the existing URL and direct-upload fields.
- **Image priority chain** — for every image slot the resolution order is: URL field (highest) → Library selection → direct upload. Existing URL and upload fields continue to work exactly as before.
- **Media Library admin thumbnail** — the Media Library list view shows an inline preview of each image for quick identification.

## [1.0.18] - 2026-03-20

### Fixed
- **Video backgrounds not playing in some browsers** — the `<source>` tag was missing a `type` attribute. Browsers such as Firefox and Safari require `type="video/mp4"` (or `video/webm` / `video/ogg`) to determine codec support before attempting playback. MIME types are now resolved from the file extension and injected automatically.
- **README rendering on the Alliance Auth app site** — horizontal rule dividers (`---`) were being rendered as literal `<hr />` tags instead of visual dividers. Removed all dividers; section headings provide sufficient separation.

## [1.0.17] - 2026-03-20

### Changed
- **PyPI publishing switched to API token auth** — replaced OIDC Trusted Publishing with a `PYPI_API_TOKEN` repository secret after repeated `invalid-publisher` OIDC exchange failures. More reliable and avoids GitHub/PyPI OIDC configuration drift.

### Fixed
- **Django 6.0 field serialization migration** — Django 6.0 re-serializes `CharField`, `BooleanField`, and `ImageField` definitions differently from earlier versions, causing `MigrationAutodetector` to detect false-positive changes. Added `0008_alter_custombranding_login_layout_and_more` to bring the recorded migration state in line with Django 6.0's output.
- **CI migration check installing latest Django** — pinned `django` to `>=4.2,<7` in the CI migration check step to prevent future Django major releases from triggering the same spurious migration detection.
- **GitHub Actions Node.js 20 deprecation warnings** — added `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true` workflow-level env var to opt all actions into Node.js 24 ahead of the June 2026 forced migration.

## [1.0.16] - 2026-03-20

### Added
- **CI migration guard** — the publish workflow now runs Django's `MigrationAutodetector` before building the package. If any model change is missing a committed migration file, the build fails with a clear error message, preventing releases that would require end-users to run `makemigrations`.
- **Automatic version stamping from git tag** — `pyproject.toml` version is overwritten by the pushed tag name in CI (`sed` from `$GITHUB_REF_NAME`), so the version in `pyproject.toml` no longer needs to be manually kept in sync with tags.

## [1.0.15] - 2026-03-19

### Added
- **Video login backgrounds** — setting the login background URL to a `.mp4`, `.webm`, `.ogv`, or `.ogg` file now plays it as a fullscreen looping video (autoplay, muted, `playsinline`). The background color field doubles as the preload color shown while the video loads. Still images and GIFs continue to work as before.

## [1.0.14] - 2026-03-19

### Security
- **Favicon URL escaping** — `mark_safe` calls around favicon URLs now escape the value first, preventing a stored XSS vector via a crafted URL in the admin.
- **CSS color field validation** — the login background color field now validates that the entered value is a safe CSS color string, rejecting expressions that could be injected into a `<style>` block.

### Added
- **PyPI publish workflow** — added `.github/workflows/publish.yml` to build and publish the package to PyPI on every version tag push using Trusted Publishing (OIDC).

## [1.0.13] - 2026-03-19

### Added
- **Split-right layout** — new `split-right` option places the login panel on the left and the background panel on the right (mirrors the existing `split` layout).
- **Split panel overlay text position** — admins can now choose Top, Center, or Bottom vertical alignment for overlay text on the background panel.
- **Split panel overlay text toggle** — a checkbox to hide overlay text entirely without clearing the text field.

## [1.0.12] - 2026-03-19

### Fixed
- **Missing `login_layout` model field** — the field was defined in the migration but absent from the model class, causing an `AttributeError` at runtime. Also added the Layout fieldset to the admin form.

## [1.0.11] - 2026-03-19

### Added
- **Login page layout selector** — admins can choose between *Centered Card* (default, login card centred over the full-page background) and *Split Screen* (background panel on the left, dark login panel on the right).

## [1.0.10] - 2026-03-19

### Fixed
- **Menu templates missing from installed package** — `templates/menu/` was not included in `package-data`, causing a `TemplateDoesNotExist` error for the AA menu override on fresh installs from PyPI.

## [1.0.9] - 2026-03-19

### Added
- **Sidebar logo override** — URL or uploaded image replaces the Alliance Auth logo in the sidebar. Configurable width in pixels.

## [1.0.8] - 2026-03-18

### Fixed
- **Navbar logo appearing inside wrong block** — logo was injected inside `header_nav_brand`, overlapping the site name. Moved outside the block so it renders alongside the name correctly.

## [1.0.7] - 2026-03-18

### Fixed
- **Admin save button missing** — `save_on_top=True` was accidentally removed in v1.0.6. Restored.

## [1.0.6] - 2026-03-18

### Fixed
- **Admin save button appearing at top only** — removed `save_on_top` so the save button returns to the bottom of the form only (reverted in v1.0.7).

## [1.0.5] - 2026-03-18

### Fixed
- **Missing migrations on fresh installs** — `0003_alter_custombranding_custom_css_and_more` and `0004_merge_20260321_0059` were not committed, causing `migrate` to fail. Both migrations added and packaged.

## [1.0.4] - 2026-03-18

### Fixed
- **Context processor install instructions incorrect** — README showed the wrong key path for appending to `TEMPLATES`. Corrected to `TEMPLATES[0]["OPTIONS"]["context_processors"]`.

## [1.0.3] - 2026-03-18

### Fixed
- **Change and view permissions missing after migrations** — `0003_restore_change_view_permissions` restores the `change_custombranding` and `view_custombranding` permissions that were dropped by the auto-generated `0002` migration.

## [1.0.2] - 2026-03-18

### Changed
- Added `save_on_top=True` to the `CustomBrandingAdmin` so the save button appears at both the top and bottom of the form.

## [1.0.1b] - 2026-03-18

### Changed
- Restructured package layout: moved app into `aa_customizer/` subfolder and fixed packaging configuration so all templates and static files are included.
- Renamed admin title to *Customizer*.

## [1.0.0] - 2026-03-18

### Added
- Initial release of **aa-customizer**.
- `CustomBranding` singleton model (via `django-solo`) with fields for: site name, login background (URL / upload / color), login logo (URL / upload / max-width), login page title and subtitle, login extra HTML, custom favicon (URL / upload), navbar logo (URL / upload / height), custom CSS (URL + inline), and extra `<head>` HTML.
- Context processor (`aa_customizer.context_processors.aa_customizer`) exposing the `AA_CUSTOMIZER` object in all templates.
- Template overrides for `public/base.html` (login page) and `allianceauth/base-bs5.html` (authenticated pages) applying all configured branding.
- Django admin interface for managing all settings from a single page.
- Migrations, static files, and packaging configuration for distribution via PyPI.

[1.0.18]: https://github.com/Thrainkrilleve/aa-customizer/compare/v1.0.17...v1.0.18
[1.0.17]: https://github.com/Thrainkrilleve/aa-customizer/compare/v1.0.16...v1.0.17
[1.0.16]: https://github.com/Thrainkrilleve/aa-customizer/compare/v1.0.15...v1.0.16
[1.0.15]: https://github.com/Thrainkrilleve/aa-customizer/compare/v1.0.14...v1.0.15
[1.0.14]: https://github.com/Thrainkrilleve/aa-customizer/compare/v1.0.13...v1.0.14
[1.0.13]: https://github.com/Thrainkrilleve/aa-customizer/compare/v1.0.12...v1.0.13
[1.0.12]: https://github.com/Thrainkrilleve/aa-customizer/compare/v1.0.11...v1.0.12
[1.0.11]: https://github.com/Thrainkrilleve/aa-customizer/compare/v1.0.10...v1.0.11
[1.0.10]: https://github.com/Thrainkrilleve/aa-customizer/compare/v1.0.9...v1.0.10
[1.0.9]: https://github.com/Thrainkrilleve/aa-customizer/compare/v1.0.8...v1.0.9
[1.0.8]: https://github.com/Thrainkrilleve/aa-customizer/compare/v1.0.7...v1.0.8
[1.0.7]: https://github.com/Thrainkrilleve/aa-customizer/compare/v1.0.6...v1.0.7
[1.0.6]: https://github.com/Thrainkrilleve/aa-customizer/compare/v1.0.5...v1.0.6
[1.0.5]: https://github.com/Thrainkrilleve/aa-customizer/compare/v1.0.4...v1.0.5
[1.0.4]: https://github.com/Thrainkrilleve/aa-customizer/compare/v1.0.3...v1.0.4
[1.0.3]: https://github.com/Thrainkrilleve/aa-customizer/compare/v1.0.2...v1.0.3
[1.0.2]: https://github.com/Thrainkrilleve/aa-customizer/compare/v1.0.1b...v1.0.2
[1.0.1b]: https://github.com/Thrainkrilleve/aa-customizer/compare/v1.0.0...v1.0.1b
[1.0.0]: https://github.com/Thrainkrilleve/aa-customizer/releases/tag/v1.0.0
