import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import "./custom.scss";
import {VBTooltipPlugin} from "bootstrap-vue";

Vue.config.productionTip = false;

new Vue({
  router,
  render: (h) => h(App),
}).$mount("#app");

Vue.use(VBTooltipPlugin);
