#!/usr/bin/env bash
set -euo pipefail

APP_USER="biometric"
APP_GROUP="biometric"
APP_DIR="/opt/biometric-sync"
APP_APP="$APP_DIR/app"
VENV_DIR="$APP_DIR/venv"
ENV_DIR="/etc/biometric-sync"
ENV_FILE="$ENV_DIR/biometric-sync.env"
SERVICE="biometric-sync.service"

# --- 0) Prasyarat OS ---
apt-get update -y
apt-get install -y python3-venv python3-pip git logrotate

# --- 1) User & direktori ---
id -u "$APP_USER" >/dev/null 2>&1 || useradd --system --create-home --home-dir /var/lib/$APP_USER --shell /usr/sbin/nologin $APP_USER
mkdir -p "$APP_DIR" "$APP_APP" "$ENV_DIR" "$APP_APP/logs"

# --- 2) Virtualenv (buat jika belum ada) ---
if [ ! -x "$VENV_DIR/bin/python" ]; then
  python3 -m venv "$VENV_DIR"
fi
"$VENV_DIR/bin/pip" install --upgrade pip

# --- 3) Kode aplikasi ---
# Asumsikan script dijalankan di root repo, copy isi repo ke $APP_DIR (kecuali .git, venv)
rsync -a --delete --exclude '.git' --exclude 'venv' ./ "$APP_DIR"/

# --- 4) ENV aman di /etc + symlink di kode ---
touch "$ENV_FILE"
chown root:"$APP_GROUP" "$ENV_FILE"
chmod 0640 "$ENV_FILE"
ln -sf "$ENV_FILE" "$APP_DIR/.env"
ln -sf "$ENV_FILE" "$APP_APP/.env"

# --- 5) Install deps (pinned) ---
if [ -f "$APP_DIR/requirements.txt" ]; then
  "$VENV_DIR/bin/pip" install -r "$APP_DIR/requirements.txt"
fi

# --- 6) Ownership ---
chown -R "$APP_USER":"$APP_GROUP" "$APP_APP"
chown -R root:root "$VENV_DIR" || true
chmod -R a+rx "$VENV_DIR" || true
chown -R "$APP_USER":"$APP_GROUP" "$APP_APP/logs"

# --- 7) systemd unit + drop-ins ---
cat > /etc/systemd/system/$SERVICE <<EOF
[Unit]
Description=ERPNext Biometric Sync Tool
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=$APP_APP
ExecStart=$VENV_DIR/bin/python erpnext_sync.py
Restart=always
EnvironmentFile=$ENV_FILE
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF

mkdir -p /etc/systemd/system/$SERVICE.d

# run-as (user, group, working dir, RW logs)
cat > /etc/systemd/system/$SERVICE.d/run-as-biometric.conf <<EOF
[Service]
User=$APP_USER
Group=$APP_GROUP
WorkingDirectory=$APP_APP
ReadWritePaths=$APP_APP/logs
EOF

# hardening fase-1
cat > /etc/systemd/system/$SERVICE.d/hardening-1.conf <<'EOF'
[Service]
NoNewPrivileges=true
PrivateTmp=true
EOF

# hardening fase-2
cat > /etc/systemd/system/$SERVICE.d/hardening-2.conf <<'EOF'
[Service]
ProtectSystem=full
ProtectHome=read-only
EOF

# --- 8) logrotate ---
cat > /etc/logrotate.d/biometric-sync <<'EOF'
/opt/biometric-sync/app/logs/*.log {
    weekly
    rotate 8
    missingok
    compress
    delaycompress
    notifempty
    copytruncate
}
EOF

# --- 9) enable & start + self-check ---
systemctl daemon-reload
systemctl enable "$SERVICE"
systemctl restart "$SERVICE"

echo "== STATUS =="
systemctl status "$SERVICE" --no-pager || true
echo "== LAST LOGS =="
journalctl -u "$SERVICE" -n 50 --no-pager || true
