# Folder Structure

This document explains the organization of the IntelliCharge Home Assistant integration.

## Directory Layout

```
intellicharge_integration/
├── custom_components/          # Home Assistant custom component
│   └── intellicharge/          # Main integration package
│       ├── __init__.py         # Integration setup and coordinator
│       ├── api.py              # IntelliCharge API client
│       ├── config_flow.py      # UI configuration flow
│       ├── const.py            # Constants and configuration
│       ├── manifest.json       # Integration metadata
│       ├── sensor.py           # Sensor platform implementation
│       └── strings.json        # UI translations
│
├── README.md                   # Main documentation
├── INSTALL.md                  # Detailed installation guide
├── QUICKSTART.md               # 5-minute quick start
├── CHANGELOG.md                # Version history
├── STRUCTURE.md                # This file
├── LICENSE                     # MIT License
├── examples.yaml               # Automations and dashboards
└── .gitignore                  # Git ignore rules
```

## File Descriptions

### Core Integration Files

#### `custom_components/intellicharge/__init__.py`
- Entry point for the integration
- Sets up the data coordinator
- Manages integration lifecycle (setup/unload)
- Defines update interval (15 minutes)
- Handles platform loading

**Key Components:**
- `async_setup_entry()` - Sets up the integration
- `async_unload_entry()` - Cleans up on removal
- `IntelliChargeDataUpdateCoordinator` - Manages data updates

#### `custom_components/intellicharge/api.py`
- API client for IntelliCharge
- Handles authentication and token management
- Makes API calls to fetch data
- Automatic token refresh on expiration

**Key Components:**
- `IntelliChargeAPI` - Main API client class
- `_get_access_token()` - Authentication
- `async_get_data()` - Fetch energy data

#### `custom_components/intellicharge/sensor.py`
- Defines all sensor entities
- 24 sensors total across 4 categories
- Proper device classes and units
- State handling and availability checks

**Sensor Categories:**
1. **Realized Performance** (7 sensors)
   - Consumed, Produced, Purchased, Sold Energy
   - Net Cost, Purchase Cost, Sell Revenue

2. **No System Comparison** (4 sensors)
   - What costs would be without solar

3. **Self Consumption** (5 sensors)
   - Performance in self-consumption mode

4. **Savings Summary** (6 sensors)
   - Savings calculations and percentages

#### `custom_components/intellicharge/config_flow.py`
- User interface for configuration
- Validates credentials during setup
- Creates config entries
- Prevents duplicate configurations

#### `custom_components/intellicharge/manifest.json`
- Integration metadata
- Dependencies (aiohttp)
- Version information
- Integration classification

#### `custom_components/intellicharge/strings.json`
- UI text translations
- Error messages
- Configuration prompts

#### `custom_components/intellicharge/const.py`
- Domain constant
- Shared configuration values

### Documentation Files

#### `README.md`
- Feature overview
- Installation methods
- Configuration guide
- Sensor descriptions
- Dashboard examples
- Troubleshooting

**Sections:**
- Features
- Installation (HACS + Manual)
- Configuration
- Sensor examples
- Dashboard examples
- Troubleshooting
- API details

#### `INSTALL.md`
- Detailed step-by-step installation
- Prerequisites
- Multiple installation methods
- Finding inverter ID
- Post-installation verification
- Comprehensive troubleshooting
- Uninstallation guide

**Sections:**
- Prerequisites
- Installation steps
- Verification
- Troubleshooting
- Configuration examples
- Updating

#### `QUICKSTART.md`
- 5-minute quick start
- Minimal steps to get running
- Common first-time issues
- Success checklist

#### `CHANGELOG.md`
- Version history
- Release notes
- Planned features
- Breaking changes

#### `examples.yaml`
- Ready-to-use automations
- Dashboard configurations
- Script examples
- Template sensors

**Contains:**
- Daily/Monthly report automations
- Alert automations
- 7 different dashboard layouts
- Template sensors for custom metrics
- Export scripts

### Other Files

#### `LICENSE`
- MIT License
- Usage rights
- Liability disclaimer

#### `.gitignore`
- Excludes Python cache files
- Ignores IDE files
- Prevents committing sensitive data

## Installation Paths

### Where Files Should Go

On your Home Assistant system:

```
/config/
└── custom_components/
    └── intellicharge/
        ├── __init__.py
        ├── api.py
        ├── config_flow.py
        ├── const.py
        ├── manifest.json
        ├── sensor.py
        └── strings.json
```

Only the `custom_components/intellicharge/` folder needs to be installed. The documentation files are for reference.

## Data Flow

```
User Input (UI)
    ↓
config_flow.py (validates credentials)
    ↓
__init__.py (creates coordinator)
    ↓
api.py (fetches data from IntelliCharge)
    ↓
IntelliChargeDataUpdateCoordinator (processes data)
    ↓
sensor.py (creates sensor entities)
    ↓
Home Assistant (displays data)
```

## Update Cycle

Every 15 minutes:
1. Coordinator triggers update
2. API client fetches latest data (last 30 days)
3. Data is processed and cached
4. All sensors update their states
5. Dashboard reflects new values

## Extending the Integration

### Adding New Sensors

1. Open `sensor.py`
2. Add sensor to the `sensors` list in `async_setup_entry()`
3. Create appropriate sensor class instance
4. Follow naming conventions

### Modifying Update Interval

Edit `__init__.py`:
```python
UPDATE_INTERVAL = timedelta(minutes=15)  # Change this value
```

### Adding New API Endpoints

1. Add method to `api.py`
2. Update coordinator in `__init__.py`
3. Create new sensors in `sensor.py`

### Supporting Multiple Inverters

Would require:
1. Update config flow to accept multiple IDs
2. Create separate coordinators per inverter
3. Namespace sensors by inverter

## Code Organization Principles

### Separation of Concerns
- **API Layer** (`api.py`) - External communication only
- **Coordinator** (`__init__.py`) - Data management and updates
- **Sensors** (`sensor.py`) - State representation only
- **Config** (`config_flow.py`) - User interaction only

### Error Handling
- API errors caught and logged
- Sensors show unavailable on errors
- Automatic retry on token expiration
- User-friendly error messages

### Home Assistant Standards
- Uses async/await throughout
- Proper type hints
- Device and entity registries
- Translation support ready
- Follows naming conventions

## Dependencies

### Required
- `aiohttp` >= 3.8.0 (HTTP client)
- Home Assistant >= 2023.1

### Optional (for examples)
- `custom:bar-card` (for comparison charts)
- `custom:sankey-chart` (for energy flow)
- `custom:apexcharts-card` (for trends)

## Testing

### Manual Testing Checklist
- [ ] Installation completes without errors
- [ ] Configuration flow works
- [ ] Authentication succeeds
- [ ] All 24 sensors appear
- [ ] Sensors update after 15 minutes
- [ ] Data displays correctly
- [ ] Currency is correct
- [ ] Uninstallation cleans up properly

### API Testing
```bash
# Test authentication
curl 'https://api.intellicharge.ai/api/v1/login/access-token' \
  --data-raw 'username=xxx&password=xxx'

# Test data fetch
curl 'https://api.intellicharge.ai/api/v2/product/pvms-ems/saving/period?inverter_id=571&start_date=2025-01-01&end_date=2025-01-31' \
  -H 'authorization: Bearer YOUR_TOKEN'
```

## Future Improvements

### Planned Enhancements
- Multiple inverter support
- Configurable date ranges
- Historical data beyond 30 days
- Energy dashboard integration
- Battery state monitoring
- Real-time updates (if supported)

### Code Quality
- Add unit tests
- Integration tests
- Type checking with mypy
- Linting with ruff/pylint
- Documentation coverage

## Support Resources

- Home Assistant Developers Docs: https://developers.home-assistant.io/
- IntelliCharge API Documentation: https://api.intellicharge.ai/docs
- HACS: https://hacs.xyz/
- Community Forum: https://community.home-assistant.io/
