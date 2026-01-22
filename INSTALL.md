# Installation Instructions

## Prerequisites

- Home Assistant version 2023.1 or newer
- IntelliCharge account with PVMS-EMS system
- Your IntelliCharge credentials (username, password)
- Your inverter ID

## Finding Your Inverter ID

Your inverter ID can be found in several ways:

1. **From the IntelliCharge web interface**: Log in and check your system settings
2. **From API calls**: If you've used the API before, it's the `inverter_id` parameter
3. **Contact IntelliCharge support**: They can provide your inverter ID

## Installation Steps

### Option 1: Install via HACS (Easiest)

1. **Ensure HACS is installed** in your Home Assistant
   - If not, follow the [HACS installation guide](https://hacs.xyz/docs/setup/download)

2. **Add Custom Repository**:
   - Open HACS in Home Assistant
   - Click on "Integrations"
   - Click the three dots (⋮) in the top right
   - Select "Custom repositories"
   - Add the repository URL: `https://github.com/yourusername/intellicharge-ha`
   - Category: "Integration"
   - Click "Add"

3. **Install the Integration**:
   - Search for "IntelliCharge" in HACS
   - Click "Download"
   - Restart Home Assistant

4. **Configure**:
   - Go to Settings → Devices & Services
   - Click "+ Add Integration"
   - Search for "IntelliCharge"
   - Follow the configuration wizard

### Option 2: Manual Installation

1. **Download the Integration**:
   - Download the `custom_components/intellicharge` folder
   - Or clone the repository:
     ```bash
     cd /config
     git clone https://github.com/yourusername/intellicharge-ha
     ```

2. **Copy to Home Assistant**:
   ```bash
   # SSH into your Home Assistant or use the File Editor add-on
   cd /config
   mkdir -p custom_components
   cp -r intellicharge_integration/custom_components/intellicharge custom_components/
   ```

3. **Restart Home Assistant**:
   - Go to Settings → System → Restart
   - Or use the command line: `ha core restart`

4. **Verify Installation**:
   - Check Home Assistant logs for any errors:
     ```bash
     ha core logs
     ```
   - Look for lines mentioning "intellicharge"

5. **Configure the Integration**:
   - Go to Settings → Devices & Services
   - Click "+ Add Integration"
   - Search for "IntelliCharge"
   - Enter your credentials:
     - Username: Your IntelliCharge username
     - Password: Your IntelliCharge password
     - Inverter ID: Your inverter ID (e.g., "571")

## Post-Installation

### Verify Sensors Are Created

After configuration, check that sensors appear:

1. Go to **Settings → Devices & Services**
2. Find "IntelliCharge" in the list
3. Click on it to see all created sensors

You should see 24 sensors organized by:
- Realized performance
- No system comparison
- Self consumption
- Savings summary

### Check Data Updates

The sensors update every 15 minutes. To verify:

1. Check any sensor's "Last Updated" timestamp
2. Look at the sensor history to see data points
3. Check Home Assistant logs for any API errors

### Troubleshooting Common Issues

#### Integration Doesn't Appear

**Problem**: IntelliCharge doesn't show up in the Add Integration list

**Solutions**:
1. Ensure you restarted Home Assistant after copying files
2. Check that files are in the correct location: `/config/custom_components/intellicharge/`
3. Verify file permissions (should be readable by Home Assistant)
4. Check logs for Python errors:
   ```bash
   grep -i "intellicharge" /config/home-assistant.log
   ```

#### "Cannot Connect" Error

**Problem**: Error during setup saying it cannot connect

**Solutions**:
1. Verify your username and password are correct
2. Check you can log in to the IntelliCharge website
3. Ensure your Home Assistant has internet access
4. Try the API manually to verify it works:
   ```bash
   curl 'https://api.intellicharge.ai/api/v1/login/access-token' \
     --data-raw 'username=YOUR_USERNAME&password=YOUR_PASSWORD'
   ```

#### Sensors Show "Unavailable"

**Problem**: Sensors exist but show as unavailable

**Solutions**:
1. Check Home Assistant logs for API errors
2. Verify your inverter ID is correct
3. Check that the IntelliCharge API is accessible
4. Wait 15 minutes for the first update cycle
5. Try reloading the integration:
   - Settings → Devices & Services → IntelliCharge → ⋮ → Reload

#### Wrong Currency

**Problem**: Sensors show the wrong currency

**Solution**: The currency is pulled from your IntelliCharge account settings. Update it there, then reload the integration.

## Uninstallation

To remove the integration:

1. **Remove Configuration**:
   - Go to Settings → Devices & Services
   - Find IntelliCharge
   - Click the three dots (⋮)
   - Select "Delete"

2. **Remove Files** (if desired):
   ```bash
   rm -rf /config/custom_components/intellicharge
   ```

3. **Restart Home Assistant**

## Updating the Integration

### Via HACS

1. Open HACS
2. Go to Integrations
3. Find IntelliCharge
4. Click "Update" if available
5. Restart Home Assistant

### Manual Update

1. Download the latest version
2. Replace the files in `/config/custom_components/intellicharge/`
3. Restart Home Assistant

## Getting Help

If you encounter issues:

1. **Check the Logs**:
   ```bash
   ha core logs | grep -i intellicharge
   ```

2. **Enable Debug Logging** (in configuration.yaml):
   ```yaml
   logger:
     default: info
     logs:
       custom_components.intellicharge: debug
   ```

3. **Create an Issue**: Include:
   - Home Assistant version
   - Integration version
   - Relevant log excerpts (remove sensitive data!)
   - Steps to reproduce the issue

## Configuration Examples

### Customize Update Interval

If you want to change the update frequency, you can modify the integration. The default is 15 minutes, but you can adjust this by editing `__init__.py`:

```python
UPDATE_INTERVAL = timedelta(minutes=30)  # Change to 30 minutes
```

### Create Lovelace Dashboard

Example dashboard configuration:

```yaml
type: vertical-stack
cards:
  - type: markdown
    content: '## IntelliCharge Energy Summary'
  - type: entities
    entities:
      - entity: sensor.consumed_energy
        name: Total Consumption
      - entity: sensor.produced_energy
        name: Solar Production
      - entity: sensor.purchased_energy
        name: Grid Import
      - entity: sensor.sold_energy
        name: Grid Export
  - type: markdown
    content: '## Financial Summary'
  - type: entities
    entities:
      - entity: sensor.net_cost
        name: Net Cost
      - entity: sensor.savings_vs_no_system
        name: Savings vs No Solar
      - entity: sensor.savings_vs_no_system_pct
        name: Savings Percentage
```

## Next Steps

After installation:

1. Create dashboards to visualize your data
2. Set up automations based on energy production/consumption
3. Create alerts for unusual patterns
4. Track your savings over time

For more examples and use cases, see the [README.md](README.md).
