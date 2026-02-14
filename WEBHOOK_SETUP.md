# Telegram Bot Webhook Setup Guide

## Prerequisites
- VPS with Ubuntu/Debian
- Domain name pointing to your VPS IP
- Root or sudo access

## Step 1: Install Required Packages

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip python3-venv -y

# Install Nginx
sudo apt install nginx -y

# Install Certbot for Let's Encrypt SSL
sudo apt install certbot python3-certbot-nginx -y
```

## Step 2: Setup Your Bot

```bash
# Create bot directory (if not exists)
cd /opt
sudo mkdir tg-bot
sudo chown $USER:$USER tg-bot
cd tg-bot

# Upload your files (bot-webhook.py, requirements.txt, .env)

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Step 3: Configure Environment Variables

Edit `.env` file:
```env
BOT_TOKEN=your_actual_bot_token
WEBHOOK_URL=https://yourdomain.com
WEBHOOK_PORT=8443
WEBHOOK_PATH=/telegram-webhook
LISTEN_ADDRESS=0.0.0.0
LISTEN_ADDRESS=0.0.0.0
```

## Step 4: Setup SSL Certificate

```bash
# Get SSL certificate from Let's Encrypt (replace with your domain and email)
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com --email your@email.com --agree-tos --no-eff-email

# Certbot will automatically configure nginx with SSL
```

## Step 5: Configure Nginx

1. Copy `nginx-example.conf` to nginx sites-available:
```bash
sudo cp nginx-example.conf /etc/nginx/sites-available/your-bot.conf
```

2. Edit the file and replace:
   - `yourdomain.com` with your actual domain
   - `/etc/letsencrypt/live/yourdomain.com/` with your certbot cert path

3. Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/your-bot.conf /etc/nginx/sites-enabled/
```

4. Test and reload nginx:
```bash
sudo nginx -t
sudo systemctl reload nginx
```

## Step 6: Open Firewall Port

```bash
# Allow HTTPS
sudo ufw allow 443/tcp
sudo ufw allow 80/tcp

# Allow local webhook port (optional, for testing)
sudo ufw allow 8443/tcp

# Check firewall status
sudo ufw status
```

## Step 7: Run Bot Manually (for testing)

```bash
cd /opt/tg-bot
source venv/bin/activate
python bot-webhook.py
```

## Step 8: Setup Systemd Service (for auto-start)

Create service file:
```bash
sudo nano /etc/systemd/system/telegram-bot.service
```

Add this content:
```ini
[Unit]
Description=Telegram Bot Webhook
After=network.target nginx.service

[Service]
Type=simple
User=your_username
WorkingDirectory=/opt/tg-bot
Environment="PATH=/opt/tg-bot/venv/bin"
ExecStart=/opt/tg-bot/venv/bin/python /opt/tg-bot/bot-webhook.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot
sudo systemctl status telegram-bot
```

## Step 9: Verify Webhook

Check logs:
```bash
# Bot logs
sudo journalctl -u telegram-bot -f

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

Test in Telegram:
1. Open your bot
2. Send `/start`
3. You should receive a response

## Troubleshooting

### Bot not responding:
1. Check if service is running: `sudo systemctl status telegram-bot`
2. Check bot logs: `sudo journalctl -u telegram-bot -n 50`
3. Check if webhook is listening: `sudo netstat -tlnp | grep 8443`

### Nginx errors:
1. Test nginx config: `sudo nginx -t`
2. Check nginx logs: `sudo tail -f /var/log/nginx/error.log`
3. Make sure port 443 is open: `sudo ufw status`

### SSL certificate issues:
1. Renew certificate: `sudo certbot renew`
2. Check cert path in nginx config matches actual path
3. Verify domain DNS points to your VPS IP

### Webhook not set:
1. Check .env WEBHOOK_URL is correct
2. Check webhook path matches nginx location path
3. Restart bot after changing .env: `sudo systemctl restart telegram-bot`
