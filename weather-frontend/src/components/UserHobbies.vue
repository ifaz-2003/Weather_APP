<template>
  <div :class="['weather-container', currentWeatherClass]">
    <div class="contained">
      <div class="header">
        <div class="menu-icon" v-if="!isDropdownVisible" @click="toggleDropDown">
          <i class="fa-solid fa-bars"></i>
        </div>

        <!-- Dropdown menu -->
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

        <!-- logout -->
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
        </div>
      </div>

      <h2 class="page-title">Hobbies for {{ city }}</h2>

      <!-- hobbies display -->
      <div class="hobbies-container">
        <div class="card" v-for="(hobby, index) in hobbies" :key="index">
          <h3>{{ hobby.name }}</h3>
          <p>{{ hobby.description }}</p>
          <a :href="hobby.link" target="_blank" class="learn-more">Learn More</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  data() {
    return {
      isDropdownVisible: false,
      isLogoutPromptVisible: false,
      username: "",
      city: "Unknown",
      temperature: null,
      hobbies: [],
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
          console.error("Failed to parse condition from weatherData:", e);
        }
      }
      return "sunny"; 
    }
  },
  methods: {
    toggleDropDown() {
      this.isDropdownVisible = !this.isDropdownVisible;
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
    getTemperature() {
      const weatherData = localStorage.getItem("weatherData");

      if (weatherData) {
        try {
          const parsedWeather = JSON.parse(weatherData);
          if (parsedWeather.temp) {
            this.temperature = parseFloat(parsedWeather.temp);
          }
        } catch (error) {
          console.error("Error parsing weatherData:", error);
        }
      }

      // fetchHobbies is now moved to run after city is set
    },
    getCity() {
      const weatherData = localStorage.getItem("weatherData");

      if (weatherData) {
        try {
          const parsedWeather = JSON.parse(weatherData);
          if (parsedWeather.city) {
            this.city = parsedWeather.city;

            // fetch hobbies based on city searched
            this.fetchHobbies();
          }
        } catch (error) {
          console.error("Error parsing weatherData:", error);
        }
      }
    },
    fetchHobbies() {
      // some  possible hobbies mapped based on weather conditions
      const hobbyMappings = {
        cold: [
          { name: "Knitting", description: "Create warm clothes for the season." },
          { name: "Baking", description: "Warm up by baking some treats." },
          { name: "Reading", description: "Cozy up with a good book by the fireplace." },
          { name: "Puzzle Solving", description: "Engage in challenging puzzles and brain teasers." }
        ],
        cool: [
          { name: "Hiking", description: "Enjoy the fresh air with a scenic hike." },
          { name: "Photography", description: "Capture stunning landscapes." },
          { name: "Fishing", description: "Relax by the water and catch some fish." },
          { name: "Birdwatching", description: "Observe and identify birds in nature." }
        ],
        moderate: [
          { name: "Cycling", description: "Perfect weather for a bike ride." },
          { name: "Yoga", description: "Practice yoga in the fresh air." },
          { name: "Gardening", description: "Grow your own flowers or vegetables." },
          { name: "Outdoor Picnics", description: "Enjoy a meal outside with friends or family." }
        ],
        warm: [
          { name: "Swimming", description: "Cool off by going for a swim." },
          { name: "Outdoor Sports", description: "Great time for tennis, football, or basketball." },
          { name: "Camping", description: "Spend a night under the stars." },
          { name: "Kayaking", description: "Paddle through rivers or lakes." }
        ],
        hot: [
          { name: "Beach Day", description: "Enjoy the sun at the beach." },
          { name: "Smoothie Making", description: "Stay refreshed with a homemade smoothie." },
          { name: "Ice Skating (Indoor)", description: "Cool down while skating indoors." },
          { name: "Water Balloon Fights", description: "Have fun with friends and family while cooling off." }
        ]
      };

      let category = "moderate";
      //hobbies are also taken into account by temperature 
      if (this.temperature !== null) {
        if (this.temperature < 5) {
          category = "cold";
        } else if (this.temperature >= 5 && this.temperature < 15) {
          category = "cool";
        } else if (this.temperature >= 15 && this.temperature < 25) {
          category = "moderate";
        } else if (this.temperature >= 25 && this.temperature < 35) {
          category = "warm";
        } else {
          category = "hot";
        }
      }

      this.hobbies = (hobbyMappings[category] || []).map((hobby) => ({
        ...hobby,
        link: `https://www.google.com/search?q=${encodeURIComponent(hobby.name + " in " + this.city)}`
      }));
    },
  },
  mounted() {
    this.getUserInfo();
    this.getTemperature();
    this.getCity();
  },
};
</script>



<style scoped>
@import "@/assets/style.css";

/*  css styles consistent through all components */
.hobbies-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
  margin-top: 20px;
  justify-content: center;
}

.dropdown-menu {
  position: fixed;
  top: 0;
  left: 0;
  width: 250px;
  height: 100vh;
  background-color: var(--bg-color2);
  padding: 20px;
  z-index: 1000;
  text-align: left;
}


.card {
  background-color: var(--bg-color2);
  padding: 15px;
  border-radius: 15px;
  color: white;
  text-align: center;
}

.card h3 {
  margin-bottom: 10px;
  font-size: 20px;
}

.card p {
  font-size: 14px;
  opacity: 0.9;
}

.learn-more {
  display: inline-block;
  margin-top: 10px;
  padding: 8px 12px;
  background-color: grey;
  color: white;
  text-decoration: none;
  border-radius: 10px;
  transition: 0.3s ease;
}

.learn-more:hover {
  background-color: darkgrey;
}

.page-title {
  margin-top: 20px;
  font-size: 28px;
  text-align: center;
  color: white;
}

.contained {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
  color: white;
  box-sizing: border-box;
}

.menu-icon {
  position: fixed;
  top: 30px;
  left: 30px;
  z-index: 1100; /* Above the menu */
}



</style>
