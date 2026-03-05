Deploy checklist to production (safe path):

Local pre-check
cd /home/devlight/Desktop/panaceya
git status
./.venv/bin/python manage.py check
Commit + push
git add -A
git commit -m "UI updates: centered section titles, deposits title move, section icons"
git push origin main
SSH to VPS
ssh <your_sudo_user>@144.172.98.156
Backup current state (quick rollback point)
cd /srv/panaceya/current
sudo -u panaceya git rev-parse --short HEAD
sudo -u panaceya git tag -f pre_deploy_$(date +%Y%m%d_%H%M%S)
Pull latest code
sudo -u panaceya git fetch --all
sudo -u panaceya git checkout main
sudo -u panaceya git pull origin main
Install dependencies (safe even if unchanged)
sudo -u panaceya /srv/panaceya/venv/bin/pip install -r /srv/panaceya/current/requirements.txt
Migrate + collect static
sudo -u panaceya /srv/panaceya/venv/bin/python manage.py migrate --settings=panaceya.settings_prod
sudo -u panaceya /srv/panaceya/venv/bin/python manage.py collectstatic --noinput --settings=panaceya.settings_prod
Restart app
sudo systemctl restart panaceya
sudo systemctl status panaceya --no-pager
Nginx check + reload
sudo nginx -t
sudo systemctl reload nginx
Smoke test
curl -I http://127.0.0.1:8010 -H "Host: 144.172.98.156"
curl -I http://144.172.98.156
