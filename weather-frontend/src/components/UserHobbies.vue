<template>
  <div :class="['weather-container', backgroundClass]">
    <video autoplay loop muted playsinline v-if="backgroundVideo" class="weather-video">
      <source :src="backgroundVideo" type="video/mp4" />
    </video>
    
    <div class="container">
      <div class="header">
        <div class="menu-icon" @click="toggleDropDown">
          <i class="fa-solid fa-bars"></i>
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
import weatherBackground from "@/stores/weatherBackground.js";

export default {
  computed: {
    backgroundClass(){
      return weatherBackground.backgroundClass;
    },

    backgroundVideo(){
      return weatherBackground.backgroundVideo;
    }

  },
  data() {
    return {
      isDropdownVisible: false,
      isLogoutPromptVisible: false, 

      username: "",
      city: "Unknown",

      temperature: null,
      hobbies: []
    };
  },
  methods: {
    toggleDropDown() {
      this.isDropdownVisible = !this.isDropdownVisible;
    },

    showLogoutPrompt() {
    this.isLogoutPromptVisible = true; // Show logout confirmation
    },

    cancelLogout() {
      this.isLogoutPromptVisible = false; // Hide logout confirmation
    },

    confirmLogout() {
      localStorage.removeItem("access_token"); // Clear user session
      this.isLogoutPromptVisible = false; // Hide popup
      this.$router.push("/login"); // Redirect to login page
    },

    getUserInfo() {
      this.username = localStorage.getItem("username") || "Guest";
    },
    getTemperature() {
      const weatherData = localStorage.getItem("weatherData");

      if (weatherData) {
        try {
          const parsedWeather = JSON.parse(weatherData);
          console.log("Retrieved weatherData:", parsedWeather); // Debugging Log

          if (parsedWeather.temp) {
            this.temperature = parseFloat(parsedWeather.temp); // Ensure it's a number
            console.log("Extracted temperature:", this.temperature, "°C");
          } else {
            console.warn("Temperature data missing from weatherData");
          }
        } catch (error) {
          console.error("Error parsing weatherData:", error);
        }
      } else {
        console.warn("No weatherData found in localStorage");
      }

      this.fetchHobbies();
    },

    getCity() {
      const weatherData = localStorage.getItem("weatherData");

      if (weatherData) {
        try {
          const parsedWeather = JSON.parse(weatherData);
          console.log("Retrieved weatherData:", parsedWeather); // Debugging Log

          if (parsedWeather.city) {
            this.city = parsedWeather.city;
            console.log("Extracted city:", this.city);
          } else {
            console.warn("City data missing from weatherData");
          }
        } catch (error) {
          console.error("Error parsing weatherData:", error);
        }
      } else {
        console.warn("No weatherData found in localStorage");
      }
    },

    fetchHobbies() {
      console.log("Fetching hobbies for temperature:", this.temperature, "°C"); // Debugging Log

      const hobbyMappings = {
        cold: [
          { name: "Knitting", description: "Create warm clothes for the season.", link: "https://www.ravelry.com/" },
          { name: "Baking", description: "Warm up by baking some treats.", link: "https://www.kingarthurbaking.com/" },
          { name: "Reading", description: "Cozy up with a good book by the fireplace.", link: "https://www.goodreads.com/" },
          { name: "Puzzle Solving", description: "Engage in challenging puzzles and brain teasers.", link: "https://www.jigsawplanet.com/" }
        ],
        cool: [
          { name: "Hiking", description: "Enjoy the fresh air with a scenic hike.", link: "https://www.alltrails.com/" },
          { name: "Photography", description: "Capture stunning landscapes.", link: "https://www.photographyblog.com/tutorials" },
          { name: "Fishing", description: "Relax by the water and catch some fish.", link: "https://www.takemefishing.org/" },
          { name: "Birdwatching", description: "Observe and identify birds in nature.", link: "https://www.audubon.org/" }
        ],
        moderate: [
          { name: "Cycling", description: "Perfect weather for a bike ride.", link: "https://www.bicycling.com/" },
          { name: "Yoga", description: "Practice yoga in the fresh air.", link: "https://www.yogajournal.com/" },
          { name: "Gardening", description: "Grow your own flowers or vegetables.", link: "https://www.gardeners.com/" },
          { name: "Outdoor Picnics", description: "Enjoy a meal outside with friends or family.", link: "https://www.bbcgoodfood.com/howto/guide/best-ever-picnic-recipes" }
        ],
        warm: [
          { name: "Swimming", description: "Cool off by going for a swim.", link: "https://www.swimming.org/" },
          { name: "Outdoor Sports", description: "Great time for tennis, football, or basketball.", link: "https://www.sportengland.org/" },
          { name: "Camping", description: "Spend a night under the stars.", link: "https://www.rei.com/learn/expert-advice/camping-beginners.html" },
          { name: "Kayaking", description: "Paddle through rivers or lakes.", link: "https://paddling.com/" }
        ],
        hot: [
          { name: "Beach Day", description: "Enjoy the sun at the beach.", link: "https://www.visitcalifornia.com/beaches/" },
          { name: "Smoothie Making", description: "Stay refreshed with a homemade smoothie.", link: "https://www.allrecipes.com/recipes/138/drinks/smoothies/" },
          { name: "Ice Skating (Indoor)", description: "Cool down while skating indoors.", link: "https://www.iceskating.org/" },
          { name: "Water Balloon Fights", description: "Have fun with friends and family while cooling off.", link: "https://www.wikihow.com/Organize-a-Water-Balloon-Fight" }
        ]
      };

      // Determine the temperature category
      let category = "moderate"; // Default category
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

      this.hobbies = hobbyMappings[category] || [
        { name: "Explore New Skills", description: "Discover new hobbies based on your interests.", link: "https://www.skillshare.com/" }
      ];

      console.log("Selected hobbies:", this.hobbies); // Debugging Log
    }
  },
  mounted() {
    this.getUserInfo();
    this.getTemperature();
    this.getCity();
  }
};


</script>

<style scoped>
@import "@/assets/style.css";

.hobbies-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
  margin-top: 20px;
  justify-content: center;
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
</style>
