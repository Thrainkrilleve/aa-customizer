# AA Customizer

A branding & customization plugin for [Alliance Auth](https://allianceauth.readthedocs.io).

Gives administrators a simple admin-panel UI to customize their Alliance Auth installation without touching code or replacing static files.


## Screenshots

### Split Screen layout
![Split Screen layout](https://i.imgur.com/4TSEjOG.png)

### Centered Card layout (default)
![Centered Card layout](https://i.imgur.com/GaTmrDD.png)

### Side Bar Icon
![Sidebar Icon](https://i.imgur.com/HG7hRYo.png)


## Features

| Feature | What it does |
|---|---|
| **Custom site name** | Overrides `SITE_NAME` from `local.py` across the whole site |
| **Login background** | URL or uploaded image/video; falls back to a CSS color, then the default AA space background. `.mp4`, `.webm`, `.ogv` URLs play as a fullscreen looping video |
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


## Requirements

- Alliance Auth ≥ 4.0.0 (Bootstrap 5 template set)
- `django-solo`
- `Pillow`


## Installation

### Bare Metal install

**1 — Install the package**

```bash
# Activate your Alliance Auth virtualenv first, then:
pip install aa-customizer
```

**2 — Add to `INSTALLED_APPS`**

Open your `local.py` and add above INSTALLED_APPS =:
```python
INSTALLED_APPS.insert(0, 'aa_customizer')
```

> Django searches each app's `templates/` folder in `INSTALLED_APPS` order and uses the first match.
> Placing `aa_customizer` first ensures its template overrides are picked up before the Alliance Auth originals.

**3 — Add the context processor**

In `local.py`, add to the settings section to append the existing `TEMPLATES` list:

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

Only needed if you want to use **file uploads or the media library** instead of image URLs.

Add these two lines anywhere in the Custom Settings section of your `local.py`:

```python
MEDIA_ROOT = "/path/to/your/media/"
MEDIA_URL  = "/media/"
```

Make sure your web server (nginx, Apache, etc.) is configured to serve files from `MEDIA_ROOT` at `MEDIA_URL`.

In your `nginx.conf`, add inside the `server {}` block:

```nginx
# Allow uploads up to 20 MB (nginx default is 1 MB — raise this if you
# get "413 Request Entity Too Large" when uploading background images).
client_max_body_size 20m;
# add after location /static
location /media {
    alias /var/www/myauth/media;
    autoindex off;
}
```

> Adjust `client_max_body_size` to suit your largest file. A 1920×1080 JPEG is typically 1–5 MB; a short MP4 video background can be 10–20 MB. Set it slightly above your expected maximum.

**7 — (Optional) Populate the Media Library**

Once media is configured, go to **AA Customizer → Media Library** in the admin panel to upload images. Give each one a descriptive name (e.g. "Corp logo v2", "Winter background"). You can then pick from your library in **Custom Branding** without re-uploading — just change the dropdown selection to switch images instantly.


### Docker install

The recommended approach for Docker is to use **URL fields** for all images (point at an external CDN, Imgur, GitHub raw assets, etc.) so you don't need to mount a media volume just to serve a few files.

**1 — Install the package inside the container**

```bash
# Activate your Alliance Auth virtualenv first, then:
pip install aa-customizer
```


Add `aa-customizer` to your pip requirements file (e.g. `requirements.txt` or the equivalent in your Docker setup), then rebuild:

```
auth migrate
```

```
auth collectstatic
```
```
exit
```

**2 — Add to `INSTALLED_APPS`**

Open your `local.py` and add above INSTALLED_APPS =:
```python
INSTALLED_APPS.insert(0, 'aa_customizer')
```

> Django searches each app's `templates/` folder in `INSTALLED_APPS` order and uses the first match.
> Placing `aa_customizer` first ensures its template overrides are picked up before the Alliance Auth originals.

**3 — Add the context processor**

In `local.py`, add to the settings section to append the existing `TEMPLATES` list:

```python
TEMPLATES[0]["OPTIONS"]["context_processors"].append(
    "aa_customizer.context_processors.aa_customizer"
)
```

**4 — (Optional) Configure media file serving**

If you want to upload images through the admin or use the media library instead of external URLs, follow these steps.
For most Docker installs, **using URL fields is simpler** — just paste an image link and skip all of the below.

**a) Add to `local.py`**

Add these two lines anywhere in the Custom Settings section of your `local.py`:

```python
MEDIA_ROOT = "/var/www/myauth/media/"
MEDIA_URL  = "/media/"
```

**b) Add the named volume to `docker-compose.yml`**

The standard AA Docker setup uses a named Docker volume for media. Add it in three places:

1. In `x-allianceauth-base` volumes (so gunicorn, beat, and workers all share it):
```yaml
x-allianceauth-base: &allianceauth-base
  volumes:
    # ... your existing volume mounts ...
    - media-data:/var/www/myauth/media
```

2. In the `nginx` service volumes:
```yaml
services:
  nginx:
    volumes:
      # ... your existing volume mounts ...
      - media-data:/var/www/myauth/media
```

3. In the top-level `volumes:` section:
```yaml
volumes:
  media-data:
```

**c) Configure nginx**

In your `nginx.conf`, add the following inside the `server {}` block:

```nginx
# Allow uploads up to 20 MB (nginx default is 1 MB — raise this if you
# get "413 Request Entity Too Large" when uploading background images).
client_max_body_size 20m;

location /media {
    alias /var/www/myauth/media;
    autoindex off;
}
```

> Adjust `client_max_body_size` to suit your largest file. A 1920×1080 JPEG is typically 1–5 MB; a short MP4 video background can be 10–20 MB. Set it slightly above your expected maximum.

**d) Bring the stack up**

```bash
docker compose up -d
```

**e) Fix volume permissions**

Docker creates named volumes owned by root. The AA container runs as uid/gid `61000`. Run this once after first bringing the stack up:

Confimr the uid/gid

```bash
docker compose exec allianceauth_gunicorn ls -la /var/www/myauth/media
#change using
docker compose exec -u root allianceauth_gunicorn chown -R 61000:61000 /var/www/myauth/media
```

After this, uploads made through `/admin/aa_customizer/aacustomizersettings/` will be stored under `/var/www/myauth/media/aa_customizer/` and served immediately by nginx.

**5 — Build and Restart**

```
docker compose build
docker compose down
docker compose up -d
```

## Usage

1. Log in to the Alliance Auth **admin panel** (`/admin/`).
2. **(Optional) Build your image library** — find **AA Customizer → Media Library** and upload your images there, giving each a name. You can upload as many as you like and switch between them without re-uploading.
3. Find **AA Customizer → Custom Branding** in the left-hand sidebar.
4. For each image slot, choose how to set it:
   - **Library** — pick from an image you uploaded to the Media Library (recommended when self-hosting media)
   - **URL** — paste an external link (CDN, Imgur, etc.) — always takes priority
   - **Upload** — upload a file directly into the field
5. Fill in any other fields you want and click **Save**.

Changes take effect immediately on the next page load — no server restart needed.


## Field reference

### Site

| Field | Description |
|---|---|
| **Site Name** | Overrides `SITE_NAME` from `local.py` |

### Login Page — Background

| Field | Description |
|---|---|
| **Login Background — URL** | URL of a background image **or video** (takes priority over everything). Video files (`.mp4`, `.webm`, `.ogv`) play fullscreen, looped, muted, and auto-paused by the browser when the tab is hidden |
| **Login Background — Library** | Select an image uploaded to the Media Library (takes priority over a direct upload) |
| **Login Background — Upload** | Upload a background image directly into this field |
| **Login Background Color** | CSS color fallback when no image is set, or the color shown behind a video while it loads (e.g. `#1a1a2e`) |

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
| **Login Logo — URL** | URL of a logo image (takes priority over everything) |
| **Login Logo — Library** | Select an image from the Media Library (takes priority over a direct upload) |
| **Login Logo — Upload** | Upload a logo image directly into this field |
| **Login Logo Max Width (px)** | Maximum display width of the login logo |
| **Login Page Title** | Custom heading shown above the SSO button |
| **Login Page Subtitle** | Optional description text below the title |
| **Login Page Extra HTML** | Raw HTML injected below the EVE SSO button (notices, links, etc.) |

### Favicon

| Field | Description |
|---|---|
| **Favicon — URL** | URL of a favicon image (takes priority over everything) |
| **Favicon — Library** | Select an image from the Media Library (takes priority over a direct upload) |
| **Favicon — Upload** | Upload a favicon image directly into this field |

### Navigation Bar Logo

| Field | Description |
|---|---|
| **Navbar Logo — URL** | URL of a navbar logo image (takes priority over everything) |
| **Navbar Logo — Library** | Select an image from the Media Library (takes priority over a direct upload) |
| **Navbar Logo — Upload** | Upload a navbar logo image directly into this field |
| **Navbar Logo Height (px)** | Display height of the navbar logo |

### Sidebar Logo

| Field | Description |
|---|---|
| **Sidebar Logo — URL** | URL of an image to replace the AA logo in the sidebar (takes priority over everything) |
| **Sidebar Logo — Library** | Select an image from the Media Library (takes priority over a direct upload) |
| **Sidebar Logo — Upload** | Upload a sidebar logo image directly into this field |
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


## Image recommendations

| Field | Recommended size / format |
|---|---|
| Login background (image) | ≥ 1920 × 1080 px, JPEG, PNG, or GIF |
| Login background (video) | 1920 × 1080 px, MP4 (H.264) or WebM (VP9); keep under ~15 MB for fast loads |
| Login logo | ≥ 256 × 256 px, transparent PNG |
| Favicon | ≥ 192 × 192 px, PNG or ICO |
| Navbar logo | Transparent PNG, height ≤ 64 px |
| Sidebar logo | Transparent PNG, width ≤ 256 px |


## Security notes

- **Raw HTML fields** (`Login Page Extra HTML`, `Extra <head> HTML`) are rendered without sanitization and are only editable by Django admin users (staff/superusers).
- **Custom CSS URL** is validated as a URL by Django's field validator; only `http`/`https` schemes are accepted.
- AA Customizer works alongside Alliance Auth's built-in **Custom CSS** admin (`/admin/custom_css/customcss/`). The customizer's CSS loads after the built-in one, so it takes precedence.


## License

MIT

