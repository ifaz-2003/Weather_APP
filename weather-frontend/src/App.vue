<template>
  <div id="app">
    <transition name="page-fade" mode="out-in">
      <router-view></router-view>
    </transition>
  </div>
</template>


<script>
export default {
  name: "App",
};
</script>

<style>
@import "@/assets/style.css";



.page-fade-enter-active, .page-fade-leave-active {
  transition: opacity 0.3s ease-in-out;
}
.page-fade-enter, .page-fade-leave-to {
  opacity: 0;
}

.page-fade-enter-active {
  animation: slide-in 0.3s ease-out;
}
.page-fade-leave-active {
  animation: slide-out 0.3s ease-in;
}
@keyframes slide-in {
  from {
    opacity: 0;
    transform: translateX(10px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}
@keyframes slide-out {
  from {
    opacity: 1;
    transform: translateX(0);
  }
  to {
    opacity: 0;
    transform: translateX(-10px);
  }
}
</style>
