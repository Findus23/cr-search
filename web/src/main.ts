import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import "./custom.scss";
import {VBTooltipPlugin} from "bootstrap-vue";
import VueMatomo, {Options} from "vue-matomo";

Vue.config.productionTip = false;

new Vue({
  router,
  render: (h) => h(App),
}).$mount("#app");

Vue.use(VBTooltipPlugin);
const matomoOptions = {
  siteId: "30",
  host: "https://matomo.lw1.at/",
  router,
  disableCookies: true,
} as Options;
Vue.use(VueMatomo, matomoOptions);
