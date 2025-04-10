import { createRouter, createWebHistory } from "vue-router";
import Signup from "@/components/UserSignup.vue";
import Login from "@/components/UserLogin.vue";
import WeatherApp from "@/components/WeatherApp.vue"; // Import WeatherApp
import UserHobbies from "@/components/UserHobbies.vue";
import SavedCities from "@/components/SavedCities.vue";
const routes = [
  { path: "/signup", component: Signup },
  { path: "/login", component: Login },
  { path: "/hobbies", component: UserHobbies},
  { path: "/preferences", component: SavedCities},
  { 
    path: "/weather", 
    component: WeatherApp, 
    meta: { requiresAuth: true } // Protect this route
  },
  { path: "/", redirect: "/login" } // Default route redirects to login
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Navigation Guard: Redirect users if not authenticated
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem("access_token");

  if (to.meta.requiresAuth && !isAuthenticated) {
    next("/login"); // Redirect to login if not logged in
  } else {
    next();
  }
});

export default router;
