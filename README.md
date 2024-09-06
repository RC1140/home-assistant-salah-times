# Overview

Pulls the Salah Times from https://salaahtimes.co.za/ , change your TownID [here](https://github.com/RC1140/home-assistant-salah-times/blob/master/sensor.py#L47) to match the value on the website (e.g. 8 is for Johannesburg) 

# Sample Card
```
type: markdown
content: |
  <table style="width: 100%; text-align: center;">
    <tr>
      <th>🌄 Fajr</th>
      <th>🌅 Sunrise</th>
      <th>🕛 Zuhr</th>
      <th>🕑 Asr</th>
      <th>🌇 Maghrib</th>
      <th>🌙 Isha</th>
    </tr>
    <tr>
      <td>{{ state_attr('sensor.salah_times', 'fajr') }}</td>
      <td>{{ state_attr('sensor.salah_times', 'sunrise') }}</td>
      <td>{{ state_attr('sensor.salah_times', 'zuhr') }}</td>
      <td>{{ state_attr('sensor.salah_times', 'asr') }}</td>
      <td>{{ state_attr('sensor.salah_times', 'maghrib') }}</td>
      <td>{{ state_attr('sensor.salah_times', 'isha') }}</td>
    </tr>
  </table>
```
