<template>
  <div :class="['weather-container', currentWeatherClass]">
    <div class="contained">
      <!-- Header with Dropdown Menu -->
      <div class="header">
        <div class="menu-icon" @click="toggleDropdown">
          <i class="fa-solid fa-bars"></i>
        </div>

        <!-- Dropdown Menu -->
        <transition name="slide-fade">
          <div class="dropdown-menu" v-if="isDropdownVisible">
            <button class="close-btn" @click="toggleDropdown">✖</button>
            <nav>
              <router-link to="/weather">The Weather</router-link>
            </nav>
            <nav>
              <router-link to="/hobbies">Hobbies</router-link>
            </nav>
            <nav>
              <router-link to="/preferences">Saved Cities</router-link>
            </nav>
            <nav class="logout-option">
              <router-link to="#" @click.prevent="showLogoutPrompt">Sign Out</router-link>
            </nav>
          </div>
        </transition>

        <transition name="fade">
          <div v-if="isLogoutPromptVisible" class="logout-overlay">
            <div class="logout-popup">
              <h3>Are you sure you want to sign out?</h3>
              <div class="logout-buttons">
                <button @click="confirmLogout">Yes</button>
                <button @click="cancelLogout">No</button>
              </div>
            </div>
          </div>
        </transition>

        <transition name="fade">
          <div v-if="isAddCityPromptVisible" class="add-city-overlay">
            <div class="add-city-popup">
              <h3>Are you sure you want to add {{ newCity }}?</h3>
              <div class="add-city-buttons">
                <button @click="confirmAddCity">Yes</button>
                <button @click="cancelAddCity">No</button>
              </div>
            </div>
          </div>
        </transition>
      </div>

      <!-- Main Content -->
      <h2>Saved Cities</h2>

      <!-- City Input -->
      <div class="add-city">
        <input type="text" v-model="newCity" placeholder="Enter city name" />
        <button @click="saveCity">Save City</button>
        <button type="button" id="voiceBtn" @click="startVoiceRecognition">
          <i class="fa-solid fa-microphone"></i>
        </button>
      </div>

      <!-- Saved Cities List -->
      <div class="saved-cities">
        <ul>
          <li v-for="(city, index) in savedCities" :key="index">
            <button @click="fetchWeather(city.city_name)">
              {{ city.city_name }} - {{ city.temp }}°C
            </button>
            <button @click="removeCity(city.city_name)">✖</button>
          </li>
        </ul>
      </div>

      <!-- Weather Display -->
      <div v-if="weather">
        <h3>{{ weather.city }}, {{ weather.country }}</h3>
        <p>{{ weather.temp }}°C - {{ weather.description }}</p>
        <img :src="weather.icon" alt="Weather Icon" />
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      newCity: "",
      isAddCityPromptVisible: false,
      savedCities: [], // Holds the saved cities for the logged-in user
      weather: null, // Holds the weather data for the selected city
      isDropdownVisible: false, // Controls dropdown visibility
      isLogoutPromptVisible: false, // Controls visibility of logout popup
    };
  },

  computed: {
    currentWeatherClass() {
      const stored = localStorage.getItem("weatherData");
      if (stored) {
        try {
          const condition = JSON.parse(stored).description?.toLowerCase() || "";
          if (condition.includes("clear")) return "sunny";
          if (condition.includes("cloud")) return "cloudy";
          if (condition.includes("rain") || condition.includes("drizzle") || condition.includes("thunder")) return "rainy";
          if (condition.includes("snow")) return "snowy";
        } catch (e) {
          console.error("Error reading weather description from localStorage:", e);
        }
      }
      return "sunny"; // fallback default
    }
  },


  methods: {
    // Toggle the dropdown menu
    toggleDropdown() {
      this.isDropdownVisible = !this.isDropdownVisible; // Toggle dropdown visibility
    },
    showLogoutPrompt() {
      this.isLogoutPromptVisible = true; // Show logout confirmation
    },

    speak(message) {
    return new Promise(resolve => {
      const speech = new SpeechSynthesisUtterance(message);
      speech.lang = "en-US";
      speech.rate = 1;
      speech.volume = 1;
      speech.onend = resolve;
      window.speechSynthesis.speak(speech);
    });
  },

  startVoiceRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert("Your browser does not support speech recognition.");
      return;
    }

    this.recognition = new SpeechRecognition();
    this.recognition.lang = "en-US";
    this.recognition.interimResults = false;
    this.recognition.maxAlternatives = 1;
    this.recognition.continuous = false;

    const handleError = async (errorType = "not_found") => {
      const messages = {
        not_found: "I couldn't find weather data for that city. Please try again.",
        no_speech: "I didn't hear anything. Please say the name of a city.",
        default: "Sorry, I didn't understand. Please try again.",
        invalid_city: "That city doesn't exist in our database. Please try a different city name."
      };
      
      const message = messages[errorType] || messages.default;
      await this.speak(message); // Use this.speak()
      this.startVoiceRecognition();
    };

    this.recognition.onresult = async (event) => {
      if (!event.results || !event.results[0]) {
        await handleError("no_speech");
        return;
      }

      const transcript = event.results[0][0].transcript.trim();
      if (!transcript) {
        await handleError("no_speech");
        return;
      }

      this.newCity = transcript;
      try {
        const geoResponse = await axios.get(
          `https://api.openweathermap.org/geo/1.0/direct?q=${this.newCity}&limit=1&appid=69ce9849eb65509427ae460da399e041`
        );

        if (!geoResponse.data.length) {
          await handleError("invalid_city");
          return;
        }

        await this.speak(`Found ${this.newCity}. Would you like to save this city?`);
        this.isAddCityPromptVisible = true;
      } catch (error) {
        console.error("Error:", error);
        await handleError("not_found");
      }
    };

    this.recognition.onerror = async (event) => {
      console.error("Speech recognition error:", event.error);
      const errorMap = {
        'no-speech': 'no_speech',
        'audio-capture': 'no_speech',
        'not-allowed': 'no_speech'
      };
      await handleError(errorMap[event.error] || 'default');
    };

    this.recognition.start();
  },

  async confirmAddCity() {
    this.isAddCityPromptVisible = false;
    try {
      await this.saveCity();
      await this.speak(`Successfully saved ${this.newCity}`); // Use this.speak()
    } catch (error) {
      await this.speak("Failed to save city. Please try again."); // Use this.speak()
      console.error("Save error:", error);
    }
  },

    cancelAddCity() {
      this.isAddCityPromptVisible = false; // ✅ Hide the popup
      this.newCity = ""; // ✅ Clear the city name
    },

    cancelLogout() {
      this.isLogoutPromptVisible = false; // Hide logout confirmation
    },

    confirmLogout() {
      localStorage.removeItem("access_token"); // Clear user session
      this.isLogoutPromptVisible = false; // Hide popup
      this.$router.push("/login"); // Redirect to login page
    },

    // Refresh the JWT token if it expires
    async refreshToken() {
      const refreshToken = localStorage.getItem('refresh_token');

      if (!refreshToken) {
        console.error("No refresh token found. Please log in again.");
        alert("Session expired. Please log in again.");
        return;
      }

      try {
        const response = await axios.post("http://127.0.0.1:8000/api/token/refresh/", {
          refresh: refreshToken,
        });

        localStorage.setItem('access_token', response.data.access);
        console.log("Token refreshed successfully.");
      } catch (error) {
        console.error("Error refreshing token:", error);
        alert("Failed to refresh token. Please log in again.");
      }
    },

    // Fetch saved cities for the logged-in user
    async fetchSavedCities() {
      const token = localStorage.getItem('access_token');

      if (!token) {
        console.error("No authentication token found. Please login.");
        alert("Session expired. Please login again.");
        return;
      }

      try {
        const response = await axios.get("http://127.0.0.1:8000/api/saved-cities/", {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.savedCities = response.data; // Update the saved cities list
      } catch (error) {
        if (error.response && error.response.status === 401) {
          // Token is expired, refresh it
          await this.refreshToken();
          await this.fetchSavedCities(); // Retry the request
        } else {
          console.error("Error fetching saved cities:", error);
          alert("Failed to fetch saved cities. Please try again.");
        }
      }
    },

    // Save a new city for the logged-in user
    async saveCity() {
      if (!this.newCity.trim()) return alert("Enter a valid city name.");

      const token = localStorage.getItem('access_token');

      if (!token) {
        console.error("No authentication token found. Please log in.");
        alert("Session expired. Please log in again.");
        return;
      }

      try {
        // Fetch weather data for the new city
        const geoResponse = await axios.get(
          `https://api.openweathermap.org/geo/1.0/direct?q=${this.newCity}&limit=1&appid=69ce9849eb65509427ae460da399e041`
        );

        if (!geoResponse.data.length) throw new Error("City not found");

        const { lat, lon } = geoResponse.data[0];

        const weatherResponse = await axios.get(
          `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=69ce9849eb65509427ae460da399e041`
        );
        const weatherData = weatherResponse.data;

        // Prepare the data to be sent to the backend
        const cityData = {
          city_name: this.newCity,
          temp: (weatherData.main.temp - 273.15).toFixed(2), // Convert Kelvin to Celsius
          description: weatherData.weather[0].description,
          icon: `https://openweathermap.org/img/wn/${weatherData.weather[0].icon}@2x.png`,
        };

        console.log("Saving city with data:", cityData); // Debugging statement

        // Save the city along with its weather data
        const response = await axios.post(
          "http://127.0.0.1:8000/api/save-city/",
          cityData,
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );

        console.log("Backend response:", response.data); // Debugging statement

        this.newCity = ""; // Clear the input field
        await this.fetchSavedCities(); // Refresh the list
      } catch (error) {
        if (error.response && error.response.status === 401) {
          // Token is expired, refresh it
          await this.refreshToken();
          await this.saveCity(); // Retry the request
        } else {
          console.error("Error saving city:", error.response ? error.response.data : error);
          alert("Failed to save city. Please try again.");
        }
      }
    },

    // Remove a city for the logged-in user
    async removeCity(city) {
      const token = localStorage.getItem('access_token');

      if (!token) {
        console.error("No authentication token found. Please log in.");
        alert("Session expired. Please log in again.");
        return;
      }

      try {
        await axios.delete(`http://127.0.0.1:8000/api/remove-city/${city}/`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        await this.fetchSavedCities(); // Refresh the list
      } catch (error) {
        if (error.response && error.response.status === 401) {
          // Token is expired, refresh it
          await this.refreshToken();
          await this.removeCity(city); // Retry the request
        } else {
          console.error("Error removing city:", error);
          alert("Failed to remove city.");
        }
      }
    },

    // Fetch weather data for a specific city
    async fetchWeather(city) {
      try {
        // Fetch city coordinates
        const geoResponse = await axios.get(
          `https://api.openweathermap.org/geo/1.0/direct?q=${city}&limit=1&appid=69ce9849eb65509427ae460da399e041`
        );
        const { lat, lon, name, country } = geoResponse.data[0];

        // Fetch weather data
        const weatherResponse = await axios.get(
          `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=69ce9849eb65509427ae460da399e041`
        );
        const weatherData = weatherResponse.data;

        // Update the weather object with the fetched data
        this.weather = {
          city: name,
          country: country,
          temp: (weatherData.main.temp - 273.15).toFixed(2), // Convert Kelvin to Celsius
          description: weatherData.weather[0].description,
          icon: `https://openweathermap.org/img/wn/${weatherData.weather[0].icon}@2x.png`,
        };
      } catch (error) {
        console.error("Error fetching weather data:", error);
        alert("Failed to fetch weather data.");
      }
    },
  },
  async mounted() {
    await this.fetchSavedCities(); // Fetch saved cities for the logged-in user
    if (this.savedCities.length > 0) {
      this.fetchWeather(this.savedCities[0].city_name); // Fetch weather for the first saved city
    }
  },
};
</script>


<style scoped>

/* Add these specific overrides at the top of your CSS */
.weather-container .header {
  position: fixed;
  top: 20px;
  left: 20px;
  right: auto;
  justify-content: flex-start;
  background-color: transparent;
  backdrop-filter: none;
  padding: 0;
}

.weather-container .menu-icon {
  margin-right: 0;
  padding: 10px;
}

.weather-container .dropdown-menu {
  position: fixed;
    top: 0;
    left: 0;
    width: 250px; /* Adjust width as needed */
    height: 100vh; /* Full height */
    background-color: var(--bg-color2); /* Use your theme color */
    box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
    padding: 20px;
    z-index: 1000;

    text-align: left;
}

/* Keep all your existing CSS rules below exactly as they were */
.contained {
  width: 100%;
  max-width: 1200px; /* allow it to scale wider */
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
  color: white;
  box-sizing: border-box;
}

/* Saved Cities Container */
.contained {
  max-width: 900px;
  margin: 20px auto;
  padding: 20px;
  text-align: center;
  color: white;
}

/* Position the input box at the top */
.add-city {
  display: flex;
  justify-content: center;
  margin-bottom: 20px; /* Space between input and saved cities */
  gap: 10px;
}

.add-city input {
  padding: 10px;
  border-radius: 8px;
  border: 1px solid grey;
  width: 60%;
}

.add-city button {
  padding: 10px 15px;
  background-color: grey;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.add-city button:hover {
  background-color: darkgrey;
}

/* Saved Cities Grid */
.saved-cities {
  display: flex;
  flex-direction: column; /* Stack cities below input */
  align-items: center;
  gap: 15px;
}

/* Individual City Box */
.saved-cities ul {
  list-style: none;
  padding: 0;
  width: 100%;
}

.saved-cities li {
  background-color: var(--bg-color2);
  padding: 15px;
  border-radius: 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: white;
  width: 100%;
}

/* City button for selecting weather */
.saved-cities li button:first-child {
  background-color: black;
  color: white;
  padding: 8px 12px;
  border-radius: 10px;
  border: none;
  cursor: pointer;
  flex-grow: 1;
  text-align: left;
}

.saved-cities li button:first-child:hover {
  background-color: darkgrey;
}

/* Remove button */
.saved-cities li button:last-child {
  background-color: red;
  color: white;
  padding: 5px 8px;
  border-radius: 50%;
  border: none;
  cursor: pointer;
}

.saved-cities li button:last-child:hover {
  background-color: darkred;
}

/* Blurred background effect */
.add-city-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5); /* Semi-transparent black */
  backdrop-filter: blur(5px); /* Blurring effect */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

/* Black box for add city confirmation */
.add-city-popup {
  background: var(--bg-color2); /* Match app's theme */
  padding: 20px;
  border-radius: 15px;
  color: white;
  text-align: center;
  width: 300px;
}

/* Buttons inside the add city popup */
.add-city-buttons {
  margin-top: 15px;
  display: flex;
  justify-content: space-around;
}

.add-city-buttons button {
  background-color: grey;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
}

.add-city-buttons button:hover {
  background-color: darkgrey;
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