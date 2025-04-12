<template>
  <div class="weather-container">
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
          <input v-model="username" type="text" placeholder="Username Or Email" required />
          <input v-model="password" type="password" placeholder="Password" required />
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


export default {
  data() {
    return {
      username: "",
      password: "",
      errorMessage: "",
    };
  },

  methods: {
    async login() {
      try {
        let response = await axios.post("http://127.0.0.1:8000/api/login/", {
          username: this.username,
          password: this.password,
        });

        console.log("Full Login API Response:", response.data); // Debugging
        console.log("Keys in response.data:", Object.keys(response.data));

        // Store correct username key
        if (response.data.user) {
          localStorage.setItem("username", response.data.user); // Store the correct username
        } else {
          console.warn("Username field not found in API response");
        }

        localStorage.setItem("access_token", response.data.access_token);



        // Redirect to WeatherApp after successful login
        this.$router.push("/weather");
      } catch (error) {
        this.errorMessage = "Invalid credentials";
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
  background-color: gr;
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
  overflow: hidden;
  min-height: 100vh;
}

</style>