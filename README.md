# AA Customizer

A branding & customization plugin for [Alliance Auth](https://github.com/allianceauth/allianceauth).

Gives administrators a simple admin-panel UI to customize their Alliance Auth installation without touching code or replacing static files.

---

## Screenshots

<!-- 
  To add screenshots:
  1. Open any GitHub Issue or Pull Request in this repo
  2. Drag and drop your image into the comment box — GitHub uploads it and gives you a URL like:
       https://github.com/user-attachments/assets/xxxxxxxx-...
  3. Paste that URL below, replacing the placeholder text inside the parentheses.
-->

### Split Screen layout
![Split Screen layout](https://via.placeholder.com/1200x600.png?text=Add+your+screenshot+URL+here)

### Centered Card layout (default)
![Centered Card layout](https://via.placeholder.com/1200x600.png?text=Add+your+screenshot+URL+here)

---

## Features

| Feature | What it does |
|---|---|
| **Custom site name** | Overrides `SITE_NAME` from `local.py` across the whole site |
| **Login background** | URL or uploaded image; falls back to a CSS color, then the default AA space background |
| **Login layout** | Centered Card, Split Screen (background left), or Split Screen (login left) |
| **Login logo** | URL or uploaded image shown at the top of the login card |
| **Login title & subtitle** | Welcome heading and description text on the login card |
| **Login extra HTML** | Raw HTML injected below the EVE SSO button (notices, Discord links, etc.) |
| **Custom favicon** | URL or uploaded image replacing all Alliance Auth browser-tab icons |
| **Navbar logo** | URL or uploaded image alongside the site name in the top navigation bar |
| **Sidebar logo** | URL or uploaded image replacing the Alliance Auth logo in the sidebar |
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

> **Which path is yours?**
> - Running Alliance Auth directly on a server with `pip` and a virtualenv → follow the **Bare Metal** steps.
> - Running Alliance Auth via `docker compose` → follow the **Docker** steps.

---

### Bare Metal install

**1 — Install the package**

```bash
# Activate your Alliance Auth virtualenv first, then:
pip install aa-customizer
```

**2 — Add to `INSTALLED_APPS`**

Open your `local.py` and add `"aa_customizer"` as the **first** entry:

```python
INSTALLED_APPS = [
    "aa_customizer",        # ← must come before allianceauth
    "allianceauth",
    "django.contrib.admin",
    # … rest of your apps …
]
```

> Django searches each app's `templates/` folder in `INSTALLED_APPS` order and uses the first match.
> Placing `aa_customizer` first ensures its template overrides are picked up before the Alliance Auth originals.

**3 — Add the context processor**

In `local.py`, append to the existing `TEMPLATES` list:

```python
TEMPLATES[0]["OPTIONS"]["context_processors"].append(
    "aa_customizer.context_processors.aa_customizer"
)
```

**4 — Run migrations**

```bash
python manage.py migrate aa_customizer
```

**5 — Collect static files**

```bash
python manage.py collectstatic
```

**6 — (Optional) Configure media file serving**

Only needed if you want to use **file uploads** instead of image URLs.

In `local.py`:

```python
MEDIA_ROOT = "/path/to/your/media/"
MEDIA_URL  = "/media/"
```

Make sure your web server (nginx, Apache, etc.) is configured to serve files from `MEDIA_ROOT` at `MEDIA_URL`.

---

### Docker install

The recommended approach for Docker is to use **URL fields** for all images (point at an external CDN, Imgur, GitHub raw assets, etc.) so you don't need to mount a media volume just to serve a few files.

**1 — Install the package inside the container**

Add `aa-customizer` to your pip requirements file (e.g. `requirements.txt` or the equivalent in your Docker setup), then rebuild:

```bash
docker compose build
```

Or install directly into a running container for a quick test:

```bash
docker exec -u root -i <gunicorn_container> pip install aa-customizer
```

**2 — Add to `INSTALLED_APPS`**

In your `local.py` (mounted into the container), add `"aa_customizer"` as the **first** entry:

```python
INSTALLED_APPS = [
    "aa_customizer",        # ← must come before allianceauth
    "allianceauth",
    "django.contrib.admin",
    # … rest of your apps …
]
```

**3 — Add the context processor**

```python
TEMPLATES[0]["OPTIONS"]["context_processors"].append(
    "aa_customizer.context_processors.aa_customizer"
)
```

**4 — Run migrations**

```bash
docker exec -i <gunicorn_container> python manage.py migrate aa_customizer
```

**5 — Collect static files**

```bash
docker exec -i <gunicorn_container> python manage.py collectstatic --noinput
```

**6 — (Optional) Media file uploads**

If you want to upload images through the admin instead of using URLs, you need a media volume:

In `local.py`:
```python
MEDIA_ROOT = "/home/allianceserver/aa-docker/media/"
MEDIA_URL  = "/media/"
```

Mount the volume in `docker-compose.yml` for both the gunicorn and nginx services:
```yaml
volumes:
  - ./media:/home/allianceserver/aa-docker/media
```

And configure nginx to serve it:
```nginx
location /media/ {
    alias /home/allianceserver/aa-docker/media/;
}
```

For most Docker installs, **using URL fields is simpler** — just paste an image link and skip all of the above.

---

## Usage

1. Log in to the Alliance Auth **admin panel** (`/admin/`).
2. Find **AA Customizer → Custom Branding** in the left-hand sidebar.
3. Fill in whichever fields you want to customize and click **Save**.

Changes take effect immediately on the next page load — no server restart needed.

---

## Field reference

### Site

| Field | Description |
|---|---|
| **Site Name** | Overrides `SITE_NAME` from `local.py` |

### Login Page — Background

| Field | Description |
|---|---|
| **Login Background — URL** | URL of a background image (takes priority over an upload) |
| **Login Background — Upload** | Uploaded background image (bare metal / media volume only) |
| **Login Background Color** | CSS color fallback when no image is set (e.g. `#1a1a2e`) |

### Login Page — Layout

| Field | Description |
|---|---|
| **Login Page Layout** | `Centered Card` — login card centered over the full-page background (default). `Split Screen — Background Left` — background on the left, dark login panel on the right. `Split Screen — Login Left` — mirrors it. |
| **Split Panel — Show Overlay Text** | Tick to show text on the background panel; untick to hide it entirely |
| **Split Panel — Overlay Text** | Text shown on the background panel. Leave blank to auto-display the site name |
| **Split Panel — Text Position** | Vertical position of the overlay text: `Top`, `Center`, or `Bottom` |

### Login Page — Branding

| Field | Description |
|---|---|
| **Login Logo — URL** | URL of a logo image (takes priority) |
| **Login Logo — Upload** | Uploaded logo image |
| **Login Logo Max Width (px)** | Maximum display width of the login logo |
| **Login Page Title** | Custom heading shown above the SSO button |
| **Login Page Subtitle** | Optional description text below the title |
| **Login Page Extra HTML** | Raw HTML injected below the EVE SSO button (notices, links, etc.) |

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

### Sidebar Logo

| Field | Description |
|---|---|
| **Sidebar Logo — URL** | URL of an image to replace the AA logo in the sidebar (takes priority) |
| **Sidebar Logo — Upload** | Uploaded sidebar logo image |
| **Sidebar Logo Width (px)** | Display width of the sidebar logo |

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
| Sidebar logo | Transparent PNG, width ≤ 256 px |

---

## Security notes

- **Raw HTML fields** (`Login Page Extra HTML`, `Extra <head> HTML`) are rendered without sanitization and are only editable by Django admin users (staff/superusers).
- **Custom CSS URL** is validated as a URL by Django's field validator; only `http`/`https` schemes are accepted.
- AA Customizer works alongside Alliance Auth's built-in **Custom CSS** admin (`/admin/custom_css/customcss/`). The customizer's CSS loads after the built-in one, so it takes precedence.

---

## License

MIT

