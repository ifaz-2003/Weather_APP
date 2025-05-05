<template>
  <div :class="['weather-container', currentWeatherClass]">
    <div class="auth-container">
      <h1>iU Weather</h1>
      <nav>
      <!-- initial page links -->
        <router-link to="/">Home</router-link>
        <router-link to="/feature">Feature</router-link>
        <router-link to="/faq">FAQ?</router-link>
      </nav>
      <div class="login-box">
        <h2>Frequently Asked Questions</h2>
        <ul class="faq-list">
          <li><strong>Q:</strong> Do I need an account?<br><strong>A:</strong> Yes, to save cities and access voice features.</li>
          <li><strong>Q:</strong> Why is the voice login not accurate?<br><strong>A:</strong> It depends on browser and pronunciation. Type is always available as fallback.</li>
          <li><strong>Q:</strong> Where does the weather data come from?<br><strong>A:</strong> OpenWeather API.</li>
          <li><strong>Q:</strong> Can I use this on any laptop/computer?<br><strong>A:</strong> Yes, it's responsive.</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import weatherBackground from "@/stores/weatherBackground"; //weather backgrounds 

export default {
  name: "AppFAQ",
  computed: {
    currentWeatherClass() {
      return weatherBackground.currentClass || "sunny";
    }
  }
};
</script>

<style scoped> 
.auth-container {
  max-width: 1200px;
  margin: auto;
  text-align: center;
  padding: 20px;
  border-radius: 10px;
}

h1 {
  color: black;
  font-size: 2.5rem;
  margin-bottom: 20px;
}

nav {
  margin-bottom: 30px;
}

nav a {
  margin: 0 15px;
  text-decoration: none;
  color: black;
  font-weight: bold;
}

nav a:hover {
  color: darkgrey;
}

.login-box {
  background-color: black;
  padding: 20px;
  border-radius: 8px;
  color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  max-width: 500px;
  margin: auto;
}

.faq-list {
  list-style-type: none;
  padding-left: 0;
  text-align: left;
}

.faq-list li {
  margin-bottom: 15px;
}

.weather-container {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  overflow: hidden;
  padding: 20px;
}

.weather-container.sunny {
  background-image: url('@/assets/sunny.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}
.weather-container.cloudy {
  background-image: url('@/assets/cloudy.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}
.weather-container.rainy {
  background-image: url('@/assets/rainy.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}
.weather-container.snowy {
  background-image: url('@/assets/snowy.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}
</style>
