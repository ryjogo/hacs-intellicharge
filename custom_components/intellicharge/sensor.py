"""Sensor platform for IntelliCharge integration."""
from __future__ import annotations

import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CURRENCY_DOLLAR,
    UnitOfEnergy,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import IntelliChargeDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

DOMAIN = "intellicharge"


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up IntelliCharge sensors from a config entry."""
    coordinator: IntelliChargeDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    sensors = [
        # Realized (actual performance)
        IntelliChargeEnergySensor(
            coordinator,
            "realised_consumed",
            "Consumed Energy",
            "realised",
            "consumed",
        ),
        IntelliChargeEnergySensor(
            coordinator,
            "realised_produced",
            "Produced Energy",
            "realised",
            "produced",
        ),
        IntelliChargeEnergySensor(
            coordinator,
            "realised_purchased",
            "Purchased Energy",
            "realised",
            "amount_purchased",
        ),
        IntelliChargeEnergySensor(
            coordinator,
            "realised_sold",
            "Sold Energy",
            "realised",
            "amount_sold",
        ),
        IntelliChargeCostSensor(
            coordinator,
            "realised_net_cost",
            "Net Cost",
            "realised",
            "net_cost",
        ),
        IntelliChargeCostSensor(
            coordinator,
            "realised_purchase_cost",
            "Purchase Cost",
            "realised",
            "total_purchase_cost",
        ),
        IntelliChargeCostSensor(
            coordinator,
            "realised_sell_revenue",
            "Sell Revenue",
            "realised",
            "total_sell_revenue",
        ),
        # No system comparison
        IntelliChargeEnergySensor(
            coordinator,
            "no_system_consumed",
            "No System - Consumed Energy",
            "no_system",
            "consumed",
        ),
        IntelliChargeEnergySensor(
            coordinator,
            "no_system_purchased",
            "No System - Purchased Energy",
            "no_system",
            "amount_purchased",
        ),
        IntelliChargeCostSensor(
            coordinator,
            "no_system_net_cost",
            "No System - Net Cost",
            "no_system",
            "net_cost",
        ),
        IntelliChargeCostSensor(
            coordinator,
            "no_system_purchase_cost",
            "No System - Purchase Cost",
            "no_system",
            "total_purchase_cost",
        ),
        # Self consumption
        IntelliChargeEnergySensor(
            coordinator,
            "self_consumption_consumed",
            "Self Consumption - Consumed Energy",
            "self_consumption",
            "consumed",
        ),
        IntelliChargeEnergySensor(
            coordinator,
            "self_consumption_produced",
            "Self Consumption - Produced Energy",
            "self_consumption",
            "produced",
        ),
        IntelliChargeEnergySensor(
            coordinator,
            "self_consumption_purchased",
            "Self Consumption - Purchased Energy",
            "self_consumption",
            "amount_purchased",
        ),
        IntelliChargeCostSensor(
            coordinator,
            "self_consumption_net_cost",
            "Self Consumption - Net Cost",
            "self_consumption",
            "net_cost",
        ),
        IntelliChargeCostSensor(
            coordinator,
            "self_consumption_purchase_cost",
            "Self Consumption - Purchase Cost",
            "self_consumption",
            "total_purchase_cost",
        ),
        # Summary/Savings
        IntelliChargeCostSensor(
            coordinator,
            "savings_realised_vs_no_system",
            "Savings vs No System",
            "summary",
            "realised_to_no_system",
        ),
        IntelliChargeCostSensor(
            coordinator,
            "savings_realised_vs_self_consumption",
            "Savings vs Self Consumption",
            "summary",
            "realised_to_self_consumption",
        ),
        IntelliChargeCostSensor(
            coordinator,
            "savings_self_consumption_vs_no_system",
            "Self Consumption Savings vs No System",
            "summary",
            "self_consumption_to_no_system",
        ),
        IntelliChargePercentageSensor(
            coordinator,
            "savings_realised_vs_no_system_pct",
            "Savings vs No System (%)",
            "summary",
            "realised_to_no_system_pct",
        ),
        IntelliChargePercentageSensor(
            coordinator,
            "savings_realised_vs_self_consumption_pct",
            "Savings vs Self Consumption (%)",
            "summary",
            "realised_to_self_consumption_pct",
        ),
        IntelliChargePercentageSensor(
            coordinator,
            "savings_self_consumption_vs_no_system_pct",
            "Self Consumption Savings vs No System (%)",
            "summary",
            "self_consumption_to_no_system_pct",
        ),
    ]

    async_add_entities(sensors)


class IntelliChargeSensorBase(CoordinatorEntity, SensorEntity):
    """Base class for IntelliCharge sensors."""

    def __init__(
        self,
        coordinator: IntelliChargeDataUpdateCoordinator,
        sensor_id: str,
        name: str,
        category: str,
        field: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._category = category
        self._field = field
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_{sensor_id}"
        self._attr_name = name
        self._attr_has_entity_name = True

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self.coordinator.config_entry.entry_id)},
            "name": "IntelliCharge",
            "manufacturer": "IntelliCharge",
            "model": "PVMS-EMS",
        }

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return (
            self.coordinator.last_update_success
            and self.coordinator.data is not None
            and "comparison" in self.coordinator.data
        )

    def _get_value(self):
        """Get the value from coordinator data."""
        if not self.available:
            return None

        if self._category == "summary":
            return self.coordinator.data.get("summary", {}).get(self._field)
        else:
            return (
                self.coordinator.data.get("comparison", {})
                .get(self._category, {})
                .get(self._field)
            )


class IntelliChargeEnergySensor(IntelliChargeSensorBase):
    """Energy sensor for IntelliCharge."""

    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
    _attr_state_class = SensorStateClass.TOTAL

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self._get_value()


class IntelliChargeCostSensor(IntelliChargeSensorBase):
    """Cost sensor for IntelliCharge."""

    _attr_device_class = SensorDeviceClass.MONETARY
    _attr_state_class = SensorStateClass.TOTAL

    @property
    def native_unit_of_measurement(self):
        """Return the unit of measurement."""
        if self.coordinator.data:
            currency = self.coordinator.data.get("comparison", {}).get("currency", "DKK")
            return currency
        return "DKK"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self._get_value()


class IntelliChargePercentageSensor(IntelliChargeSensorBase):
    """Percentage sensor for IntelliCharge."""

    _attr_native_unit_of_measurement = "%"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        value = self._get_value()
        if value is not None:
            # Convert decimal to percentage (0.13 -> 13)
            return round(value * 100, 2)
        return None
