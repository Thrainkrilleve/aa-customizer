# AA Customizer

A branding & customization plugin for [Alliance Auth](https://github.com/allianceauth/allianceauth).

Gives administrators a simple admin-panel UI to customize their Alliance Auth installation without touching code or replacing static files. Every image field supports both a **URL** and a direct **file upload** — URL always wins — making this plugin fully usable in Docker installs where a media volume may not be practical.

| Feature | What it does |
|---|---|
| **Custom site name** | Overrides `SITE_NAME` from `local.py` across the whole site |
| **Login background** | URL or uploaded image; falls back to a CSS color, then the default AA space background |
| **Login logo** | URL or uploaded image shown at the top of the login card |
| **Login title & subtitle** | Welcome heading and description text on the login card |
| **Login extra HTML** | Raw HTML injected below the EVE SSO button (notices, Discord links, etc.) |
| **Custom favicon** | URL or uploaded image replacing all Alliance Auth browser-tab icons |
| **Navbar logo** | URL or uploaded image alongside the site name in the top navigation bar |
| **Custom CSS — URL** | External stylesheet linked in every page `<head>`, loaded after the active theme |
| **Custom CSS — inline** | CSS text injected via `<style>` on every page, loaded after the active theme |
| **Extra `<head>` HTML** | Raw HTML at the end of `<head>` on every page (analytics, font imports, meta tags) |

---

## Requirements

- Alliance Auth ≥ 4.0.0 (Bootstrap 5 template set)
- `django-solo`
- `Pillow`

---

## Installation

### 1 — Install the package

```bash
pip install aa-customizer
# or, from source:
pip install /path/to/aa-customizer
```

### 2 — Add to `INSTALLED_APPS`

Open your `local.py` and add `"aa_customizer"` **before** the core Alliance Auth apps so that the template overrides take priority:

```python
INSTALLED_APPS = [
    "aa_customizer",        # ← must come first
    "allianceauth",
    "django.contrib.admin",
    # … rest of your apps …
]
```

> **Why first?**  Django's `APP_DIRS` template loader searches each installed
> app's `templates/` folder in `INSTALLED_APPS` order and uses the first match.
> `aa_customizer` ships overrides for `allianceauth/icons.html`,
> `allianceauth/base-bs5.html`, `public/base.html`, and `public/login.html`.
> Placing it first ensures these overrides are picked up instead of the
> Alliance Auth originals.  Each override gracefully falls back to default
> Alliance Auth behaviour when no customization is configured.

### 3 — Add the context processor

In your `local.py`, append the context processor to the existing `TEMPLATES` list.
The standard Alliance Auth `local.py` imports from `base.py`, so the `TEMPLATES` setting already exists — you just need to append to it:

```python
# local.py — add AFTER your imports / INSTALLED_APPS block
TEMPLATES[0]["OPTIONS"]["context_processors"].append(
    "aa_customizer.context_processors.aa_customizer"
)
```

> **Why not redefine `TEMPLATES`?**  Your `local.py` starts with `from .base import *`, so `TEMPLATES` is already defined by Alliance Auth's `base.py`.  Appending keeps all existing context processors intact and avoids duplicating the full block.

### 4 — Run migrations

```bash
python manage.py migrate aa_customizer
```

### 5 — Collect static files

```bash
python manage.py collectstatic
```

### 6 — (Optional) Configure media file serving

Only needed if you use **file uploads** rather than URLs.  Skip this step for Docker installs where you set image URLs instead.

Make sure `MEDIA_ROOT` and `MEDIA_URL` are configured and that your web server (nginx, etc.) serves files from that directory:

```python
# local.py
MEDIA_ROOT = "/path/to/your/media/"
MEDIA_URL  = "/media/"
```

For development (not production), add this to your project `urls.py`:

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # … your urls …
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## Usage

1. Log in to the Alliance Auth **admin panel** (`/admin/`).
2. Find **AA Customizer → Custom Branding** in the left-hand sidebar.
3. Fill in whichever fields you want to customize and click **Save**.

Changes take effect immediately on the next page load — no server restart needed.

---

## Docker / URL-first workflow

In containerized deployments, mounting a media volume just to serve a few images is often more trouble than it's worth.  Every image field has a companion **URL field** — set the URL and leave the upload blank.  Point the URL at:

- A public CDN or object-storage bucket (S3, R2, Backblaze B2, etc.)
- A self-hosted image URL
- Any publicly reachable image link (e.g. Imgur, GitHub raw assets)

**Priority order for each image**: URL field → uploaded file → AA default.

---

## Field reference

### Site

| Field | Description |
|---|---|
| **Site Name** | Overrides `SITE_NAME` from `local.py` |

### Login Page — Background

| Field | Description |
|---|---|
| **Login Background — URL** | URL of a background image (takes priority) |
| **Login Background — Upload** | Uploaded background image |
| **Login Background Color** | CSS color fallback (e.g. `#1a1a2e`) when no image is set |

### Login Page — Branding

| Field | Description |
|---|---|
| **Login Logo — URL** | URL of a logo image (takes priority) |
| **Login Logo — Upload** | Uploaded logo image |
| **Login Logo Max Width (px)** | Maximum display width of the login logo |
| **Login Page Title** | Custom heading on the login card |
| **Login Page Subtitle** | Optional description below the title |
| **Login Page Extra HTML** | Raw HTML injected below the EVE SSO button |

### Favicon

| Field | Description |
|---|---|
| **Favicon — URL** | URL of a favicon image (takes priority) |
| **Favicon — Upload** | Uploaded favicon image |

### Navigation Bar Logo

| Field | Description |
|---|---|
| **Navbar Logo — URL** | URL of a navbar logo image (takes priority) |
| **Navbar Logo — Upload** | Uploaded navbar logo image |
| **Navbar Logo Height (px)** | Display height of the navbar logo |

### Custom CSS

| Field | Description |
|---|---|
| **Custom CSS — URL** | External stylesheet URL linked in every page `<head>` |
| **Custom CSS** | Inline CSS injected via `<style>` on every page |

### Extra HTML

| Field | Description |
|---|---|
| **Extra `<head>` HTML** | Raw HTML injected at the end of `<head>` on every page |

---

## Image recommendations

| Field | Recommended size / format |
|---|---|
| Login background | ≥ 1920 × 1080 px, JPEG or PNG |
| Login logo | ≥ 256 × 256 px, transparent PNG |
| Favicon | ≥ 192 × 192 px, PNG or ICO |
| Navbar logo | Transparent PNG, height ≤ 64 px |

---

## Security notes

- **Raw HTML fields** (`Login Page Extra HTML`, `Extra <head> HTML`) are rendered without sanitization and are only editable by Django admin users (staff/superusers).
- **Custom CSS URL** is validated as a URL by Django's field validator; only `http`/`https` schemes are accepted.
- AA Customizer works alongside Alliance Auth's built-in **Custom CSS** admin (`/admin/custom_css/customcss/`). The customizer's CSS loads after the built-in one, so it takes precedence.

---

## License

MIT
