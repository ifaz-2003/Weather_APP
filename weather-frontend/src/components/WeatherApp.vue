<template>
  <div :class="['weather-container', backgroundClass]">
    <video autoplay loop muted playsinline v-if="backgroundVideo" class="weather-video">
      <source :src="backgroundVideo" type="video/mp4" />
    </video>

    <div class="container">
      <div class="header">
        <div class="menu-icon" @click="toggleDropDown">
          <i class="fa-solid fa-bars"></i> <!-- FontAwesome hamburger icon -->
        </div>

        <!-- Dropdown Menu -->
        <transition name="slide-fade">
          <div class="dropdown-menu" v-if="isDropdownVisible">
            <button class="close-btn" @click="toggleDropDown">✖</button>
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

        <!-- Logout Confirmation Popup -->
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

        <div class="header-left">
          <h2>Welcome, {{ username }}!</h2>
        </div>
        <div class="weather-input">
          <input type="text" name="city" id="city_input" placeholder="Enter city name" v-model="city" />
          <button type="button" id="searchBtn" @click="fetchWeather">
            <i class="fa-regular fa-search"></i> Search
          </button>
          <button type="button" id="locationBtn" @click="getUserCoordinates">
            <i class="bx bx-target-lock"></i> Current Location
          </button>
          <button type="button" id="voiceBtn" @click="startVoiceRecognition">
            <i class="fa-solid fa-microphone"></i>
          </button>
        </div>
      </div>

      <div class="weather-data">
        <div class="weather-left">
          <div class="card">
            <div class="current-weather">
              <div class="details">
                <p>Now</p>
                <h2>{{ weather.temp }}&deg;C</h2>
                <p>{{ weather.description }}</p>
              </div>
              <div class="weather-icon">
                <img :src="weather.icon" alt="Weather Icon" />
              </div>
              <button class="speaker-button" @click="speakWeather">
                <i class="fa-solid fa-volume-up"></i> <!-- Speaker Icon -->
              </button>
              <hr />
              <div class="card-footer">
                <p><i class="fa-light fa-calendar"></i>{{ weather.date }}</p>
                <p><i class="fa-light fa-location-dot"></i>{{ weather.city }}, {{ weather.country }}</p>
              </div>
            </div>
          </div>

          <div class="card">
            <h2>5 Days Forecast</h2>
            <button class="speaker-button" @click="speakAverageForecast">
              <i class="fa-solid fa-volume-up"></i> <!-- Speaker Icon -->
            </button>
            <div class="day-forecast">
              <div class="forecast-item" v-for="(day, index) in forecast" :key="index">
                <div class="icon-wrapper">
                  <img :src="day.icon" alt="Weather Icon" />
                  <span>{{ day.temp }}&deg;C</span>
                </div>
                <p>{{ day.date }}</p>
                <p>{{ day.day }}</p>
              </div>
            </div>
          </div>
        </div>

        <div class="weather-right">
          <h2>Today's Highlights</h2>
          <div class="highlights">
            <div class="card">
              <div class="card-head">
                <p>Air Quality Index</p>
                <p class="air-index aqi-1">{{ weather.airQuality }}</p>
              </div>
              <div class="air-indices">
                <i class="fa-regular fa-wind fa-3x"></i>
                <div class="item">
                  <p>PM2.5</p>
                  <h2>{{ weather.pm2_5 }}</h2>
                </div>
                <div class="item">
                  <p>PM10</p>
                  <h2>{{ weather.pm10 }}</h2>
                </div>
                <div class="item">
                  <p>SO2</p>
                  <h2>{{ weather.so2 }}</h2>
                </div>
                <div class="item">
                  <p>CO</p>
                  <h2>{{ weather.co }}</h2>
                </div>
                <div class="item">
                  <p>NO</p>
                  <h2>{{ weather.no }}</h2>
                </div>
                <div class="item">
                  <p>NO2</p>
                  <h2>{{ weather.no2 }}</h2>
                </div>
                <div class="item">
                  <p>NH3</p>
                  <h2>{{ weather.nh3 }}</h2>
                </div>
                <div class="item">
                  <p>O3</p>
                  <h2>{{ weather.o3 }}</h2>
                </div>
              </div>
            </div>
            <div class="card">
              <div class="card-head">
                <p>Sunrise & Sunset</p>
                <button class="speaker-button" @click="speakSunriseSunset">
                  <i class="fa-solid fa-volume-up"></i> <!-- Speaker Icon -->
                </button>
              </div>
              <div class="sunrise-sunset">
                <div class="item">
                  <div class="icon">
                    <i class="fa-light fa-sunrise fa-4x"></i>
                  </div>
                  <div>
                    <p>Sunrise</p>
                    <h2>{{ weather.sunrise }}</h2>
                  </div>
                </div>
                <div class="item">
                  <div class="icon">
                    <i class="fa-light fa-sunset fa-4x"></i>
                  </div>
                  <div>
                    <p>Sunset</p>
                    <h2>{{ weather.sunset }}</h2>
                  </div>
                </div>
              </div>
            </div>
            <div class="card">
              <div class="card-head">
                <p>Humidity</p>
              </div>
              <div class="card-item">
                <i class="fa-light fa-droplet fa-2x"></i>
                <h2 id="humidityVal">{{ weather.humidity }}%</h2>
              </div>
            </div>
            <div class="card">
              <div class="card-head">
                <p>Pressure</p>
              </div>
              <div class="card-item">
                <i class="fa-light fa-compass fa-2x"></i>
                <h2 id="Pressureval">{{ weather.pressure }} hPa</h2>
              </div>
            </div>
            <div class="card">
              <div class="card-head">
                <p>Visibility</p>
              </div>
              <div class="card-item">
                <i class="fa-light fa-eye fa-2x"></i>
                <h2 id="VisibilityVal">{{ weather.visibility }} km</h2>
              </div>
            </div>
            <div class="card">
              <div class="card-head">
                <p>Wind Speed</p>
              </div>
              <div class="card-item">
                <i class="fa-light fa-location-arrow fa-2x"></i>
                <h2 id="windSpeedVal">{{ weather.windSpeed }} m/s</h2>
              </div>
            </div>
            <div class="card">
              <div class="card-head">
                <p>Feels Like</p>
              </div>
              <div class="card-item">
                <i class="fa-light fa-temperature-list fa-2x"></i>
                <h2 id="feelsVal">{{ weather.feelsLike }}&deg;C</h2>
              </div>
            </div>
          </div>
          <h2>Today at</h2>
          <div class="hourly-forecast">
            <div class="card" v-for="(hour, index) in hourlyForecast" :key="index">
              <p>{{ hour.time }}</p>
              <img :src="hour.icon" alt="Weather Icon" />
              <p>{{ hour.temp }}&deg;C</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import moment from "moment";

// Weather background management
const weatherBackground = {
  backgroundClass: "",
  backgroundVideo: null
};

export default {
  data() {
    return {
      isDropdownVisible: false,
      isLogoutPromptVisible: false,
      username: "",
      city: "London",
      weather: {
        temp: "___",
        description: "_____",
        icon: "https://openweathermap.org/img/wn/04d@2x.png",
        date: moment().format("dddd, MMM DD"),
        city: "_________",
        country: "_________",
        airQuality: "Good",
        sunrise: "____",
        sunset: "____",
        humidity: "____",
        pressure: "____",
        visibility: "____",
        windSpeed: "____",
        feelsLike: "____",
        pm2_5: "____",
        pm10: "____",
        so2: "____",
        co: "____",
        no: "____",
        no2: "____",
        nh3: "____",
        o3: "____",
      },
      forecast: Array(5).fill({
        icon: "https://openweathermap.org/img/wn/02d.png",
        temp: "____",
        date: "_______",
        day: "_______",
      }),
      hourlyForecast: Array(8).fill({
        time: "9 AM",
        icon: "https://openweathermap.org/img/wn/04d.png",
        temp: "____",
      }),
      recognition: null,
    };
  },

  computed: {
    backgroundClass() {
      return weatherBackground.backgroundClass;
    },
    backgroundVideo() {
      return weatherBackground.backgroundVideo;
    },
  },

  methods: {
    async fetchWeather() {
      try {
        // Fetch city coordinates
        const geoResponse = await axios.get(
          `https://api.openweathermap.org/geo/1.0/direct?q=${this.city}&limit=1&appid=69ce9849eb65509427ae460da399e041`
        );

        if (!geoResponse.data.length) {
          throw new Error("City not found");
        }

        const { lat, lon, name, country } = geoResponse.data[0];

        // Fetch weather data
        const weatherResponse = await axios.get(
          `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=69ce9849eb65509427ae460da399e041`
        );
        const weatherData = weatherResponse.data;

        // Fetch air pollution data
        const airPollutionResponse = await axios.get(
          `https://api.openweathermap.org/data/2.5/air_pollution?lat=${lat}&lon=${lon}&appid=69ce9849eb65509427ae460da399e041`
        );
        const airPollutionData = airPollutionResponse.data.list[0].components;

        // Fetch 5-day forecast
        const forecastResponse = await axios.get(
          `https://api.openweathermap.org/data/2.5/forecast?lat=${lat}&lon=${lon}&appid=69ce9849eb65509427ae460da399e041`
        );
        const forecastData = forecastResponse.data.list;

        // Update weather data
        this.weather = {
          temp: (weatherData.main.temp - 273.15).toFixed(2),
          description: weatherData.weather[0].description,
          condition: weatherData.weather[0].main.toLowerCase(),
          icon: `https://openweathermap.org/img/wn/${weatherData.weather[0].icon}@2x.png`,
          date: moment().format("dddd, MMM DD"),
          city: name,
          country: country,
          airQuality: "Good",
          sunrise: moment.unix(weatherData.sys.sunrise).format("hh:mm A"),
          sunset: moment.unix(weatherData.sys.sunset).format("hh:mm A"),
          humidity: weatherData.main.humidity,
          pressure: weatherData.main.pressure,
          visibility: (weatherData.visibility / 1000).toFixed(1),
          windSpeed: weatherData.wind.speed,
          feelsLike: (weatherData.main.feels_like - 273.15).toFixed(2),
          pm2_5: airPollutionData.pm2_5,
          pm10: airPollutionData.pm10,
          so2: airPollutionData.so2,
          co: airPollutionData.co,
          no: airPollutionData.no,
          no2: airPollutionData.no2,
          nh3: airPollutionData.nh3,
          o3: airPollutionData.o3,
        };

        // Set the background based on the weather condition
        this.setWeatherBackground(this.weather.condition);

        localStorage.setItem(
          "weatherData",
          JSON.stringify({
            temp: this.weather.temp,
            city: this.weather.city,
            description: this.weather.description,
          })
        );

        // Update 5-day forecast
        this.forecast = forecastData
          .filter((_, index) => index % 8 === 0)
          .slice(0, 5)
          .map((item) => ({
            icon: `https://openweathermap.org/img/wn/${item.weather[0].icon}.png`,
            temp: (item.main.temp - 273.15).toFixed(2),
            date: moment(item.dt_txt).format("DD MMM"),
            day: moment(item.dt_txt).format("dddd"),
          }));

        // Update hourly forecast
        this.hourlyForecast = forecastData.slice(0, 8).map((item) => ({
          time: moment(item.dt_txt).format("h A"),
          icon: `https://openweathermap.org/img/wn/${item.weather[0].icon}.png`,
          temp: (item.main.temp - 273.15).toFixed(2),
        }));
      } catch (error) {
        console.error("Error fetching weather data:", error);
        alert("Failed to fetch weather data");
      }
    },

    speakWeather() {
      if (!this.weather.temp || !this.weather.city) {
        alert("Weather data not available for speech output.");
        return;
      }

      const message = `The weather is ${this.weather.temp} degrees Celsius in ${this.weather.city}.`;
      const speech = new SpeechSynthesisUtterance(message);
      speech.lang = "en-US";
      speech.rate = 1;
      speech.volume = 1;
      window.speechSynthesis.speak(speech);
    },

    setWeatherBackground(condition) {
      console.log("Raw weather condition:", condition);

      condition = condition.toLowerCase().trim();

      const backgrounds = {
        clear: { 
          class: "sunny", 
          video: require("@/assets/sunny.mp4") 
        },
        clouds: { 
          class: "cloudy", 
          video: require("@/assets/cloudy.mp4") 
        },
        rain: { 
          class: "rainy", 
          video: require("@/assets/rainy.mp4") 
        },
        drizzle: {
          class: "rainy",
          video: require("@/assets/rainy.mp4")
        },
        snow: { 
          class: "snowy", 
          video: require("@/assets/snowy.mp4") 
        },
        thunderstorm: {
          class: "rainy",
          video: require("@/assets/rainy.mp4")
        },
        default: { 
          class: "default-bg", 
          video: require("@/assets/sunny.mp4") 
        }
      };

      let selectedBg = backgrounds.default;
      
      if (condition.includes("clear")) {
        selectedBg = backgrounds.clear;
      } 
      else if (condition.includes("cloud")) {
        selectedBg = backgrounds.clouds;
      } 
      else if (condition.includes("rain") || condition.includes("drizzle")) {
        selectedBg = backgrounds.rain;
      } 
      else if (condition.includes("snow")) {
        selectedBg = backgrounds.snow;
      }
      else if (condition.includes("thunder")) {
        selectedBg = backgrounds.thunderstorm;
      }

      weatherBackground.backgroundClass = selectedBg.class;
      weatherBackground.backgroundVideo = selectedBg.video;
    },

    speakSunriseSunset() {
      if (!this.weather.sunrise || !this.weather.sunset) {
        alert("Sunrise and sunset data not available for speech output.");
        return;
      }

      const message = `The sunrise today is at ${this.weather.sunrise}, and the sunset is at ${this.weather.sunset}.`;
      const speech = new SpeechSynthesisUtterance(message);
      speech.lang = "en-US";
      speech.rate = 1;
      speech.volume = 1;
      window.speechSynthesis.speak(speech);
    },

    speakAverageForecast() {
      if (!this.forecast || this.forecast.length < 5) {
        alert("Not enough forecast data available.");
        return;
      }

      try {
        const temp1 = parseFloat(this.forecast[0]?.temp || 0);
        const temp2 = parseFloat(this.forecast[1]?.temp || 0);
        const temp3 = parseFloat(this.forecast[2]?.temp || 0);
        const temp4 = parseFloat(this.forecast[3]?.temp || 0);
        const temp5 = parseFloat(this.forecast[4]?.temp || 0);

        const totalTemp = temp1 + temp2 + temp3 + temp4 + temp5;
        const avgTemp = (totalTemp / 5).toFixed(2);

        const message = `The average weather over the next 5 days is ${avgTemp} degrees Celsius.`;
        const speech = new SpeechSynthesisUtterance(message);
        speech.lang = "en-US";
        speech.rate = 1;
        speech.volume = 1;
        window.speechSynthesis.speak(speech);
      } catch (error) {
        console.error("Error calculating average temperature:", error);
        alert("An error occurred while calculating the average temperature.");
      }
    },

    async getUserCoordinates() {
      try {
        const position = await new Promise((resolve, reject) => {
          navigator.geolocation.getCurrentPosition(resolve, reject);
        });
        const { latitude, longitude } = position.coords;

        const reverseGeoResponse = await axios.get(
          `https://api.openweathermap.org/geo/1.0/reverse?lat=${latitude}&lon=${longitude}&limit=1&appid=69ce9849eb65509427ae460da399e041`
        );
        const { name } = reverseGeoResponse.data[0];
        this.city = name;

        this.fetchWeather();
      } catch (error) {
        console.error("Error fetching user coordinates:", error);
        alert("Failed to fetch user location");
      }
    },

    toggleDropDown() {
      this.isDropdownVisible = !this.isDropdownVisible;
      console.log("Dropdown toggled:", this.isDropdownVisible);
    },
    
    showLogoutPrompt() {
      this.isLogoutPromptVisible = true;
    },

    cancelLogout() {
      this.isLogoutPromptVisible = false;
    },

    confirmLogout() {
      localStorage.removeItem("access_token");
      this.isLogoutPromptVisible = false;
      this.$router.push("/login");
    },

    getUserInfo() {
      this.username = localStorage.getItem("username") || "Guest";
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

      const speak = (message) => {
        return new Promise(resolve => {
          const speech = new SpeechSynthesisUtterance(message);
          speech.lang = "en-US";
          speech.rate = 1;
          speech.volume = 1;
          speech.onend = resolve;
          window.speechSynthesis.speak(speech);
        });
      };

      const handleError = async (errorType = "not_found") => {
        const messages = {
          not_found: "I couldn't find that city. Please try saying a valid city name again.",
          no_speech: "I didn't hear anything. Please say the name of a city.",
          default: "Sorry, I didn't understand. Please try again.",
          invalid_city: "That city doesn't exist in our database. Please try a different city name."
        };
        
        const message = messages[errorType] || messages.default;
        await speak(message);
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

        this.city = transcript;
        try {
          // First check if city exists by fetching coordinates
          const geoResponse = await axios.get(
            `https://api.openweathermap.org/geo/1.0/direct?q=${this.city}&limit=1&appid=69ce9849eb65509427ae460da399e041`
          );

          if (!geoResponse.data.length) {
            await handleError("invalid_city");
            return;
          }

          // Only proceed with weather fetch if city is valid
          await this.fetchWeather();
          await speak(`Showing weather for ${this.weather.city}`);
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
  },

  mounted() {
    this.getUserInfo();
    this.fetchWeather();
  },
};
</script>

<style>
@import "@/assets/style.css";
</style>