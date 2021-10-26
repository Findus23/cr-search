import Vue from "vue";
import Router from "vue-router";
import Home from "./views/Home.vue";
import Transcript from "@/views/Transcript.vue";

Vue.use(Router);

export default new Router({
  mode: "history",
  base: process.env.BASE_URL,
  routes: [
    {
      path: "/",
      redirect: "/campaign2/10/",
      name: "home"
    },
    {
      path: "/episodes",
      name: "episodes",
      component: () => import(/* webpackChunkName: "episodes" */ "./views/Episodes.vue"),
    },
    {
      path: "/transcript/:series/:episodeNr",
      name: "transcript",
      component: Transcript,
      props: true,
    },
    {
      path: "/:something/",
      redirect: "/campaign2/10/",
    },
    {
      path: "/:series/:episode/:keyword?",
      name: "search",
      component: Home,
      // props: true,
    },
  ],
});
