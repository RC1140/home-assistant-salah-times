"""Sensor platform for Salah Times."""
from __future__ import annotations

from datetime import timedelta
import logging

import requests
from bs4 import BeautifulSoup

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(hours=1)

async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up the Salah Times sensor."""
    async_add_entities([SalahTimesSensor()], True)

class SalahTimesSensor(SensorEntity):
    """Representation of a Salah Times sensor."""

    def __init__(self):
        """Initialize the sensor."""
        self._attr_name = "Salah Times"
        self._attr_unique_id = "salah_times_sensor"
        self._attr_native_value = None
        self._attr_extra_state_attributes = {}

    async def async_update(self):
        """Fetch new state data for the sensor."""
        salah_times = await self.hass.async_add_executor_job(self.fetch_salah_times)
        if salah_times:
            self._attr_native_value = salah_times[0]['date']
            self._attr_extra_state_attributes = salah_times[0]

    def fetch_salah_times(self):
        """Fetch Salah times from the website."""
        url = "https://salaahtimes.co.za/Home/GetTownSalaahTime?TownID=8&SearchFromDate=&IsShowTownTimetableOnly=true"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table', class_='table-bordered')

            if not table:
                _LOGGER.error("Table not found in the HTML")
                return None

            rows = table.find_all('tr')
            salah_times = []

            for row in rows[1:]:  # Skip the header row
                cols = row.find_all('td')
                if len(cols) >= 14:
                    date = cols[0].text.strip()
                    fajr = cols[3].text.strip()
                    sunrise = cols[4].text.strip()
                    zuhr = cols[8].text.strip()
                    asr = cols[10].text.strip()
                    maghrib = cols[12].text.strip()
                    isha = cols[13].text.strip()

                    salah_times.append({
                        "date": date,
                        "fajr": fajr,
                        "sunrise": sunrise,
                        "zuhr": zuhr,
                        "asr": asr,
                        "maghrib": maghrib,
                        "isha": isha
                    })

            return salah_times

        except requests.RequestException as e:
            _LOGGER.error(f"Error fetching data: {e}")
            return None
