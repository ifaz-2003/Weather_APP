<template>
  <div :class="['weather-container', weatherBackground.backgroundClass]">
    <video autoplay loop muted playsinline v-if="weatherBackground.backgroundVideo" class="weather-video">
      <source :src="weatherBackground.backgroundVideo" type="video/mp4" />
    </video>

    <div class="auth-container">
      <h1>iU Weather</h1>
      <nav>
        <router-link to="/">Home</router-link>
        <router-link to="/feature">Feature</router-link>
        <router-link to="/faq">FAQ?</router-link>
      </nav>
      <div class="signup-box">
        <h2>Signup</h2>
        <form @submit.prevent="signup">
          <input v-model="username" type="text" placeholder="Username" required />
          <input v-model="email" type="email" placeholder="Email" required />
          <input v-model="password1" type="password" placeholder="Password" required />
          <input v-model="password2" type="password" placeholder="Confirm Password" required />
          <button type="submit">Signup</button>
        </form>
        <p>Already have an account? <router-link to="/login">Login</router-link></p>
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import weatherBackground from "@/stores/weatherBackground";


export default {
  data() {
    return {
      username: "",
      email: "",
      password1: "",
      password2: "",
      errorMessage: "",
    };
  },

  computed:{
    weatherBackground(){
      return weatherBackground;
    }
  },

  methods: {
    async signup() {
      try {
        let response = await axios.post("http://127.0.0.1:8000/api/signup/", {
          username: this.username,
          email: this.email,
          password1: this.password1,
          password2: this.password2,
        });

        console.log("Signup API response:", response.data); // Log full response

        // Check if username exists before storing
        if (response.data.username) {
          localStorage.setItem("username", response.data.username);
        } else {
          console.warn("Username is missing from the API response");
        }



        // Store JWT token in localStorage
        localStorage.setItem("access_token", response.data.access_token);


        // Redirect to WeatherApp after successful signup
        this.$router.push("/weather");
      } catch (error) {
        this.errorMessage = "Signup failed: " + JSON.stringify(error.response.data);
      }
    },
  },
};
</script>

<style scoped>
.auth-container {
  max-width: 1200px;
  margin: auto;
  text-align: center;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

h1 {
  font-size: 2.5rem;
  color: black;
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
  color: lightgrey;
}

.signup-box {
  background-color: black;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: inline-block;
  width: 100%;
  max-width: 400px;
}

h2 {
  font-size: 1.8rem;
  margin-bottom: 20px;
  color: white;
}

input {
  width: 90%;
  padding: 10px;
  margin: 10px 0;
  border: 1px solid #b2dfdb;
  border-radius: 4px;
  font-size: 1rem;
}

button {
  width: 95%;
  padding: 10px;
  background-color: grey;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
}

button:hover {
  background-color: darkgrey;
}

p {
  margin-top: 15px;
  color: white;
}

.error-message {
  color: #d32f2f;
  margin-top: 10px;
}

.weather-video {
  position: fixed;
  top: 0;
  left: 0;
  min-width: 100vw;
  min-height: 100vh;
  object-fit: cover;
  z-index: -1;
}

.weather-container {
  position: relative;
  overflow: hidden;
  min-height: 100vh;
}

</style>