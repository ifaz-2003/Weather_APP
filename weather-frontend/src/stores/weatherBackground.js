
import { reactive } from "vue";

const weatherBackground = reactive({
  currentClass: "sunny", 
  setCondition(condition) {
    if (condition.includes("clear")) this.currentClass = "sunny";
    else if (condition.includes("cloud")) this.currentClass = "cloudy";
    else if (condition.includes("rain") || condition.includes("drizzle") || condition.includes("thunder")) this.currentClass = "rainy";
    else if (condition.includes("snow")) this.currentClass = "snowy";
    else this.currentClass = "default-bg";
  },
});

export default weatherBackground;
