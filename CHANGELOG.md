# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
