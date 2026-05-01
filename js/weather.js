  // --- Weather Banner (Austin, TX — geolocked) ---
  (function() {
    const days = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
    const months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    const now = new Date();
    const dateStr = days[now.getDay()] + ', ' + months[now.getMonth()] + ' ' + now.getDate();
    document.getElementById('wb-date').textContent = dateStr + ' · Austin, TX';

    // Weather condition → icon mapping
    function weatherIcon(code) {
      if (code === 0) return '☀️';
      if (code <= 3) return '⛅';
      if (code <= 48) return '🌫️';
      if (code <= 57) return '🌦️';
      if (code <= 65) return '🌧️';
      if (code <= 67) return '🌧️';
      if (code <= 77) return '❄️';
      if (code <= 82) return '🌧️';
      if (code <= 86) return '❄️';
      if (code >= 95) return '⛈️';
      return '⛅';
    }

    function weatherDesc(code) {
      if (code === 0) return 'Clear';
      if (code <= 3) return 'Partly cloudy';
      if (code <= 48) return 'Foggy';
      if (code <= 57) return 'Drizzle';
      if (code <= 65) return 'Rain';
      if (code <= 67) return 'Freezing rain';
      if (code <= 77) return 'Snow';
      if (code <= 82) return 'Showers';
      if (code <= 86) return 'Snow showers';
      if (code >= 95) return 'Thunderstorm';
      return 'Cloudy';
    }

    // Open-Meteo free API — no key needed, Austin coords
    fetch('https://api.open-meteo.com/v1/forecast?latitude=30.2672&longitude=-97.7431&current=temperature_2m,weather_code,wind_speed_10m&temperature_unit=fahrenheit&wind_speed_unit=mph&timezone=America%2FChicago')
      .then(r => r.json())
      .then(data => {
        const cur = data.current;
        const temp = Math.round(cur.temperature_2m);
        const code = cur.weather_code;
        const wind = Math.round(cur.wind_speed_10m);
        document.getElementById('wb-icon').textContent = weatherIcon(code);
        document.getElementById('wb-temp').textContent = temp + '°F';
        document.getElementById('wb-desc').textContent = weatherDesc(code) + ' · Wind ' + wind + ' mph';
      })
      .catch(() => {
        // Fallback: hide weather portion gracefully
        document.getElementById('wb-weather').style.display = 'none';
      });
  })();