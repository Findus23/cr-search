import Vue from "vue";
import Router from "vue-router";
import Home from "./views/Home.vue";
import Episodes from "@/views/Episodes.vue";

Vue.use(Router);

export default new Router({
  mode: "history",
  base: process.env.BASE_URL,
  routes: [
    {
      path: "/",
      redirect: "/campaign2/10/",
    },
    {
      path: "/episodes",
      name: "episodes",
        component: () => import(/* webpackChunkName: "episodes" */ "./views/Episodes.vue"),
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
    // {
    //   path: "/about",
    //   name: "about",
    //   // route level code-splitting
    //   // this generates a separate chunk (about.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: () => import(/* webpackChunkName: "about" */ "./views/About.vue"),
    // },
  ],
});
