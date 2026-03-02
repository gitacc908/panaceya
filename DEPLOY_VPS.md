# Panaceya VPS Deploy (safe with existing app)

This guide deploys Panaceya on its own process (`127.0.0.1:8010`) and its own Nginx `server_name`, so it does not replace another app.

## 1. Push code to server

From local machine:

```bash
git add .
git commit -m "Prepare production deployment"
git push origin main
```

## 2. SSH to server

```bash
ssh <sudo_user>@144.172.98.156
```

## 3. Install base packages

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip nginx git
```

## 4. Create isolated app user and folders

```bash
sudo adduser --system --group --home /srv/panaceya panaceya || true
sudo mkdir -p /srv/panaceya/current /srv/panaceya/shared/media /srv/panaceya/shared
sudo chown -R panaceya:www-data /srv/panaceya
```

## 5. Pull project code

```bash
sudo -u panaceya git clone <your_repo_url> /srv/panaceya/current || true
cd /srv/panaceya/current
sudo -u panaceya git fetch --all
sudo -u panaceya git checkout main
sudo -u panaceya git pull origin main
```

## 6. Create virtualenv and install deps

```bash
sudo -u panaceya python3 -m venv /srv/panaceya/venv
sudo -u panaceya /srv/panaceya/venv/bin/pip install --upgrade pip
sudo -u panaceya /srv/panaceya/venv/bin/pip install -r /srv/panaceya/current/requirements.txt
```

## 7. Configure production env

```bash
sudo cp /srv/panaceya/current/.env.production.example /srv/panaceya/shared/.env
sudo nano /srv/panaceya/shared/.env
```

Set at minimum:
- `DJANGO_SECRET_KEY` to a strong random value.
- `DJANGO_ALLOWED_HOSTS=144.172.98.156` for now.
- `DJANGO_CSRF_TRUSTED_ORIGINS=http://144.172.98.156` for now.

## 8. Migrate and collect static

```bash
cd /srv/panaceya/current
sudo -u panaceya /srv/panaceya/venv/bin/python manage.py migrate --settings=panaceya.settings_prod
sudo -u panaceya /srv/panaceya/venv/bin/python manage.py collectstatic --noinput --settings=panaceya.settings_prod
```

## 9. Create systemd service

```bash
sudo cp /srv/panaceya/current/deploy/systemd/panaceya.service /etc/systemd/system/panaceya.service
sudo systemctl daemon-reload
sudo systemctl enable --now panaceya
sudo systemctl status panaceya --no-pager
```

## 10. Configure Nginx for server IP first

Create a temporary Nginx file:

```bash
sudo tee /etc/nginx/sites-available/panaceya >/dev/null <<'EOF'
server {
    listen 80;
    listen [::]:80;
    server_name 144.172.98.156;

    client_max_body_size 20m;

    location /static/ { alias /srv/panaceya/current/staticfiles/; }
    location /media/ { alias /srv/panaceya/shared/media/; }

    location / {
        proxy_pass http://127.0.0.1:8010;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF
```

Enable and reload:

```bash
sudo ln -s /etc/nginx/sites-available/panaceya /etc/nginx/sites-enabled/panaceya
sudo nginx -t
sudo systemctl reload nginx
```

## 11. Verify

```bash
curl -I http://127.0.0.1:8010
curl -I http://144.172.98.156
```

## 12. Later: point domain

At domain provider:
- Add `A` record for `@` -> `144.172.98.156`
- Add `A` record for `www` -> `144.172.98.156` (optional)

When DNS propagates, update:

```bash
sudo cp /srv/panaceya/current/deploy/nginx/panaceya.conf /etc/nginx/sites-available/panaceya
sudo nano /etc/nginx/sites-available/panaceya
# confirm it uses panacea-top.to and www.panacea-top.to
sudo nginx -t
sudo systemctl reload nginx
```

Then update `/srv/panaceya/shared/.env`:
- `DJANGO_ALLOWED_HOSTS=panacea-top.to,www.panacea-top.to,144.172.98.156`
- `DJANGO_CSRF_TRUSTED_ORIGINS=https://panacea-top.to,https://www.panacea-top.to,http://144.172.98.156`

Restart app:

```bash
sudo systemctl restart panaceya
```

## 13. Optional HTTPS (Let's Encrypt)

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d panacea-top.to -d www.panacea-top.to
```
