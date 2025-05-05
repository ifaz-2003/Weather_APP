import { createRouter, createWebHistory } from "vue-router";
import Signup from "@/components/UserSignup.vue";
import Login from "@/components/UserLogin.vue";
import WeatherApp from "@/components/WeatherApp.vue"; 
import UserHobbies from "@/components/UserHobbies.vue";
import SavedCities from "@/components/SavedCities.vue";
import AppFAQ from "@/components/AppFAQ.vue";
import AppFeature from "@/components/AppFeature.vue";  //imported components

const routes = [
  { path: "/signup", component: Signup },
  { path: "/login", component: Login },
  { path: "/hobbies", component: UserHobbies},
  { path: "/preferences", component: SavedCities},
  { path: "/feature", component: AppFeature},
  { path: "/faq", component: AppFAQ},
  { 
    path: "/weather", 
    component: WeatherApp, 
    meta: { requiresAuth: true } // Route protection
  },
  { path: "/", redirect: "/login" } // Default route directs back to login
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Navigation guard: Redirect users if not authenticated
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem("access_token");

  if (to.meta.requiresAuth && !isAuthenticated) {
    next("/login"); // Redirected to login if not logged in
  } else {
    next();
  }
});

export default router;
