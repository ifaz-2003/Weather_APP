<template>
  <div :class="['weather-container', currentWeatherClass]">
    <div class="auth-container">
      <h1>iU Weather</h1>
      <nav>
        <router-link to="/">Home</router-link>
        <router-link to="/feature">Feature</router-link>
        <router-link to="/faq">FAQ?</router-link>
      </nav>
      <div class="login-box">
        <h2>App Features</h2>
        <!-- List of features -->
        <ul class="feature-list">
          <li>🌦️ Real-time weather by city or location</li>
          <li>🎤 Voice-based login and city search</li>
          <li>🧠 Hobbies suggested based on temperature</li>
          <li>📍 Save cities and see their current weather</li>
          <li>🧭 Responsive UI with dynamic backgrounds</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import weatherBackground from "@/stores/weatherBackground";

export default {
  name: "AppFeature",
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

.feature-list {
  list-style: none;
  padding-left: 0;
  text-align: left;
  font-size: 1rem;
  line-height: 1.6;
}

.feature-list li {
  margin-bottom: 15px;
}

h2 {
  font-size: 1.8rem;
  margin-bottom: 20px;
  text-align: center;
  color: white;
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
