# Changelog

All notable changes to the IntelliCharge Home Assistant Integration will be documented in this file.

## [1.0.0] - 2026-01-22

### Added
- Initial release of IntelliCharge integration
- Support for authentication with IntelliCharge API
- 24 sensors covering energy production, consumption, and costs:
  - Realized performance sensors (7 sensors)
  - No system comparison sensors (4 sensors)
  - Self-consumption mode sensors (5 sensors)
  - Savings summary sensors (6 sensors)
  - Additional percentage-based savings sensors (2 sensors)
- Automatic token refresh on expiration
- Config flow for easy setup via UI
- Support for multiple currencies (auto-detected from account)
- 15-minute update interval for near real-time data
- 30-day historical data window
- Comprehensive documentation and examples
- Support for Home Assistant 2023.1+

### Features
- **Energy Tracking**: Monitor consumed, produced, purchased, and sold energy
- **Cost Analysis**: Track net costs, purchase costs, and sell revenue
- **Savings Calculation**: Compare actual performance against:
  - No solar system scenario
  - Self-consumption only mode
- **Dashboard Ready**: All sensors include proper device classes and units
- **Currency Support**: Automatically uses account currency (DKK, EUR, USD, etc.)
- **Reliable Updates**: Automatic token management and error recovery

### Documentation
- Complete README with feature overview
- Detailed INSTALL.md with troubleshooting
- examples.yaml with automations and dashboard configurations
- Code comments and docstrings throughout

### Technical Details
- Uses aiohttp for async API calls
- Implements proper coordinator pattern for data updates
- Includes error handling and automatic retry logic
- Follows Home Assistant integration best practices
- Type hints throughout the codebase

## [Unreleased]

### Planned Features
- Historical data tracking beyond 30 days
- Configurable update intervals
- Additional statistics and trend analysis
- Support for multiple inverters in single installation
- Energy flow visualization card
- Predictive analytics based on weather
- Cost forecasting
- Custom date range selector
- Export data to CSV functionality
- Integration with Home Assistant Energy dashboard

### Under Consideration
- Real-time data updates (if API supports)
- Push notifications for significant savings
- Integration with other solar monitoring platforms
- Battery state monitoring (if available in API)
- Weather-based production forecasting
- Tariff optimization recommendations
- Comparison with neighbors (anonymized)
- Carbon footprint reduction tracking
