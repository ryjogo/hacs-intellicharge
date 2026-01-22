# IntelliCharge Home Assistant Integration

A custom Home Assistant integration for IntelliCharge PVMS-EMS systems. This integration fetches energy production, consumption, and cost data from the IntelliCharge API and creates sensors in Home Assistant.

## Features

This integration creates 24 sensors that track:

### Realized Performance (Your Actual System)
- **Energy Sensors:**
  - Consumed Energy (kWh)
  - Produced Energy (kWh)
  - Purchased Energy (kWh)
  - Sold Energy (kWh)

- **Cost Sensors:**
  - Net Cost (in your currency)
  - Purchase Cost
  - Sell Revenue

### No System Comparison
Shows what your energy usage would be without solar/battery:
- Consumed Energy
- Purchased Energy
- Net Cost
- Purchase Cost

### Self Consumption Mode
Shows performance if you only used self-consumption without smart optimization:
- Consumed Energy
- Produced Energy
- Purchased Energy
- Net Cost
- Purchase Cost

### Savings Summary
- Savings vs No System (absolute and %)
- Savings vs Self Consumption (absolute and %)
- Self Consumption Savings vs No System (absolute and %)

## Installation

### Method 1: HACS (Recommended)

1. Open HACS in Home Assistant
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL and select "Integration" as the category
6. Click "Install"
7. Restart Home Assistant

### Method 2: Manual Installation

1. Download the `custom_components/intellicharge` folder from this repository
2. Copy it to your Home Assistant `config/custom_components/` directory
3. Restart Home Assistant

## Configuration

1. In Home Assistant, go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for "IntelliCharge"
4. Enter your credentials:
   - **Username**: Your IntelliCharge login username
   - **Password**: Your IntelliCharge password
   - **Inverter ID**: Your inverter ID (e.g., "571")

The integration will create all sensors automatically.

## Sensor Examples

After setup, you'll have sensors like:

- `sensor.consumed_energy` - Total energy consumed
- `sensor.produced_energy` - Total solar energy produced
- `sensor.net_cost` - Your actual net energy cost
- `sensor.savings_vs_no_system` - How much money you've saved
- `sensor.savings_vs_no_system_pct` - Savings percentage

## Data Update Frequency

The integration updates data every **15 minutes** by default. It fetches data for the last 30 days.

## Currency Support

The integration automatically detects and uses the currency configured in your IntelliCharge account (e.g., DKK, EUR, USD).

## Dashboard Example

You can create a dashboard card to display your savings:

```yaml
type: entities
title: IntelliCharge Energy Summary
entities:
  - entity: sensor.consumed_energy
  - entity: sensor.produced_energy
  - entity: sensor.net_cost
  - entity: sensor.savings_vs_no_system
  - entity: sensor.savings_vs_no_system_pct
```

Or create a more detailed energy dashboard:

```yaml
type: grid
cards:
  - type: statistic
    entity: sensor.savings_vs_no_system
    name: Total Savings
    period:
      calendar:
        period: month
  - type: statistic
    entity: sensor.produced_energy
    name: Solar Production
    period:
      calendar:
        period: month
  - type: statistic
    entity: sensor.consumed_energy
    name: Energy Consumed
    period:
      calendar:
        period: month
```

## Troubleshooting

### Integration doesn't appear
- Make sure you've restarted Home Assistant after installation
- Check the Home Assistant logs for any error messages

### "Cannot connect" error
- Verify your username and password are correct
- Check that your inverter ID is correct
- Ensure your IntelliCharge account is active

### Sensors show "Unavailable"
- Check your internet connection
- Verify the IntelliCharge API is accessible
- Check Home Assistant logs for API errors

### Token expired errors
The integration automatically refreshes the access token when it expires. If you see persistent token errors:
1. Try removing and re-adding the integration
2. Verify your credentials are still valid

## API Details

The integration uses the IntelliCharge API v2:
- **Login endpoint**: `https://api.intellicharge.ai/api/v1/login/access-token`
- **Data endpoint**: `https://api.intellicharge.ai/api/v2/product/pvms-ems/saving/period`

## Support

For issues or feature requests, please open an issue on the GitHub repository.

## License

This integration is provided as-is for personal use with IntelliCharge systems.
