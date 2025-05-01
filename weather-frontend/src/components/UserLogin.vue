<template>
  <div :class="['weather-container', weatherClass]">
    <div class="auth-container">
      <h1>iU Weather</h1>
      <nav>
        <router-link to="/">Home</router-link>
        <router-link to="/feature">Feature</router-link>
        <router-link to="/faq">FAQ?</router-link>
      </nav>
      <div class="login-box">
        <h2>Login</h2>
        <form @submit.prevent="login">
          <div class="input-group">
            <input v-model="username" type="text" placeholder="Username or Email" required />
            <button type="button" class="voice-btn" @click="startVoiceInput('username')">
              <i class="fa-solid fa-microphone"></i>
            </button>
          </div>

          <div class="input-group">
            <input v-model="password" type="password" placeholder="Password" required />
            <button type="button" class="voice-btn" @click="startVoiceInput('password')">
              <i class="fa-solid fa-microphone"></i>
            </button>
          </div>

          <button type="submit">Login</button>
        </form>
        <p>Don't have an account? <router-link to="/signup">Sign Up Now</router-link></p>
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
      password: "",
      errorMessage: "",
    };
  },

  computed: {
    weatherClass() {
      return weatherBackground.currentClass || "sunny"; // fallback default
    }
  },

  methods: {
    async login() {
      try {
        let response = await axios.post("http://127.0.0.1:8000/api/login/", {
          username: this.username,
          password: this.password,
        });

        console.log("Full Login API Response:", response.data);

        if (response.data.user) {
          localStorage.setItem("username", response.data.user);
        } else {
          console.warn("Username field not found in API response");
        }

        localStorage.setItem("access_token", response.data.access_token);
        this.$router.push("/weather");
      } catch (error) {
        this.errorMessage = "Invalid credentials";
      }
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

        if (field === 'username') this.username = parsed;
        if (field === 'password') this.password = parsed;
      };

      recognition.onerror = (event) => {
        console.error("Speech recognition error:", event.error);
        alert("Voice input error: " + event.error);
      };

      recognition.start();
    }
  },
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
  color: darkgrey;
}

.login-box {
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
  border: 1px solid whitesmoke;
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

.weather-container.default-bg {
  background-image: url('@/assets/sunny.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

.login-box {
  background-color: black;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
  margin: auto;
  text-align: center;
}

.input-group {
  display: flex;
  align-items: center;
  width: 100%;
  margin: 10px 0;
}

.input-group input {
  flex-grow: 1;
  padding: 10px;
  font-size: 1rem;
  border-radius: 4px;
  border: 1px solid whitesmoke;
  margin-right: 8px;
  background: white;
  color: black;
}

.voice-btn {
  width: 40px;
  height: 40px;
  background-color: grey;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.voice-btn:hover {
  background-color: darkgrey;
}

button[type="submit"] {
  width: 100%;
  padding: 10px;
  background-color: grey;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  margin-top: 10px;
}

button[type="submit"]:hover {
  background-color: darkgrey;
}


</style>