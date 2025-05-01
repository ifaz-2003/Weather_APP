<template>
  <div :class="['weather-container', currentWeatherClass]">
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
          <div class="input-group">
            <input v-model="username" type="text" placeholder="Username" required />
            <button type="button" class="voice-btn" @click="startVoiceInput('username')">
              <i class="fa-solid fa-microphone"></i>
            </button>
          </div>

          <div class="input-group">
            <input v-model="email" type="email" placeholder="Email" required />
            <button type="button" class="voice-btn" @click="startVoiceInput('email')">
              <i class="fa-solid fa-microphone"></i>
            </button>
          </div>

          <div class="input-group">
            <input v-model="password1" type="password" placeholder="Password" required />
            <button type="button" class="voice-btn" @click="startVoiceInput('password1')">
              <i class="fa-solid fa-microphone"></i>
            </button>
          </div>

          <div class="input-group">
            <input v-model="password2" type="password" placeholder="Confirm Password" required />
            <button type="button" class="voice-btn" @click="startVoiceInput('password2')">
              <i class="fa-solid fa-microphone"></i>
            </button>
          </div>

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

  computed: {
    currentWeatherClass() {
      return 'sunny'; // Default background
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

        if (response.data.username) {
          localStorage.setItem("username", response.data.username);
        }

        localStorage.setItem("access_token", response.data.access_token);
        this.$router.push("/weather");
      } catch (error) {
        this.errorMessage = "Signup failed: " + JSON.stringify(error.response.data);
      }
    },

    startVoiceInput(field) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      if (!SpeechRecognition) {
        alert("Your browser does not support voice recognition.");
        return;
      }

      const recognition = new SpeechRecognition();
      recognition.lang = "en-US";
      recognition.interimResults = false;
      recognition.maxAlternatives = 1;

      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        const parsed = this.parseSpelledInput(transcript);
        this[field] = parsed;
      };

      recognition.onerror = (event) => {
        console.error("Speech recognition error:", event.error);
        alert("Voice input error: " + event.error);
      };

      recognition.start();
    },

    parseSpelledInput(transcript) {
      const map = {
        "zero": "0", "one": "1", "two": "2", "three": "3",
        "four": "4", "five": "5", "six": "6", "seven": "7",
        "eight": "8", "nine": "9",
        "dot": ".", "period": ".", "underscore": "_",
        "dash": "-", "minus": "-", "at": "@", "space": " ",
        "comma": ",", "apostrophe": "'", "quote": "\""
      };

      const words = transcript.toLowerCase().split(/[\s,-]+/);
      return words.map(w => map[w] || w[0]).join('');
    }
  }
};
</script>

<style scoped>
.auth-container {
  width: 100%;
  max-width: 500px;
  text-align: center;
  padding: 20px;
  border-radius: 10px;
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
  margin: auto;
}

h2 {
  font-size: 1.8rem;
  margin-bottom: 20px;
  color: white;
}

.input-group {
  display: flex;
  align-items: center;
  width: 100%;
  margin: 10px 0;
}

.input-group input {
  flex: 1;
  padding: 10px;
  font-size: 1rem;
  border-radius: 4px;
  border: 1px solid whitesmoke;
  margin-right: 10px;
}

.voice-btn {
  width: 36px;
  height: 36px;
  padding: 0;
  font-size: 1rem;
  border-radius: 4px;
  background-color: grey;
  color: white;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.voice-btn:hover {
  background-color: darkgrey;
}

button {
  width: 100%;
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

.weather-container {
  position: relative;
  overflow: hidden;
  min-height: 100vh;
}

.weather-container.sunny {
  background-image: url('@/assets/sunny.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}
</style>
