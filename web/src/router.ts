import Vue from "vue";
import Router from "vue-router";

Vue.use(Router);

export default new Router({
  mode: "history",
  base: process.env.BASE_URL,
  routes: [
    {
      path: "/",
      redirect: "/campaign3/10/",
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
      component: () => import(/* webpackChunkName: "transcript" */ "./views/Transcript.vue"),
      props: true,
    },
    {
      path: "/:something/",
      redirect: "/campaign2/10/",
    },
    {
      path: "/:series/:episode/:keyword?",
      name: "search",
      component: () => import(/* webpackChunkName: "search" */ "./views/Home.vue"),
      // props: true,
    },
  ],
});
