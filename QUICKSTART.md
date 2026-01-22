# Quick Start Guide

Get your IntelliCharge integration running in 5 minutes!

## Prerequisites Checklist

- [ ] Home Assistant installed and running
- [ ] IntelliCharge account credentials
- [ ] Your inverter ID (check IntelliCharge dashboard or API)
- [ ] SSH or File Editor access to Home Assistant

## Installation (3 Steps)

### Step 1: Copy Files (2 minutes)

```bash
# SSH into your Home Assistant
cd /config
mkdir -p custom_components

# Copy the intellicharge folder to custom_components
cp -r /path/to/intellicharge custom_components/
```

Or use the File Editor:
1. Create folder: `config/custom_components/intellicharge/`
2. Upload all files from the `custom_components/intellicharge/` folder

### Step 2: Restart Home Assistant (1 minute)

- Go to **Settings → System → Restart**
- Wait for restart to complete

### Step 3: Configure Integration (2 minutes)

1. Go to **Settings → Devices & Services**
2. Click **+ Add Integration**
3. Search for "IntelliCharge"
4. Enter your details:
   - Username: `your_username`
   - Password: `your_password`
   - Inverter ID: `571` (your ID)
5. Click **Submit**

## Verify Installation

Check that sensors appear:

1. Go to **Settings → Devices & Services → IntelliCharge**
2. You should see 24 sensors listed
3. Wait 15 minutes for first data update

## Create Your First Dashboard

Copy this into a new dashboard card:

```yaml
type: entities
title: My Energy Summary
entities:
  - sensor.consumed_energy
  - sensor.produced_energy
  - sensor.net_cost
  - sensor.savings_vs_no_system
```

## What's Next?

- 📊 Check out [examples.yaml](examples.yaml) for more dashboard ideas
- 🤖 Set up automations for daily reports
- 📈 Create trend graphs with ApexCharts
- 💡 Monitor your savings in real-time

## Common First-Time Issues

### "Integration not found"
**Fix**: Make sure files are in `/config/custom_components/intellicharge/` and restart HA

### "Cannot connect"
**Fix**: Double-check username, password, and inverter ID

### Sensors show "Unknown"
**Fix**: Wait 15 minutes for first update, then check logs

## Get Help

- Check [INSTALL.md](INSTALL.md) for detailed troubleshooting
- Review [README.md](README.md) for full documentation
- Check Home Assistant logs: **Settings → System → Logs**

## Success! 🎉

You should now have:
- ✅ 24 working sensors
- ✅ Real-time energy data
- ✅ Savings tracking
- ✅ Ready-to-use dashboard examples

Enjoy monitoring your IntelliCharge system!
