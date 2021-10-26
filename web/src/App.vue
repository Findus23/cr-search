<template>
    <div id="app">
        <div class="container">
            <div id="contentwrapper">
                <transition name="fade">
                    <div id="page-mask" v-if="showIntro" @click="showIntro=false"></div>
                </transition>

                <Intro v-if="showIntro"></Intro>

                <router-view/>
                <footer>
                    <button @click="showIntro=true" class="btn btn-link">About this website</button>
                    <router-link :to="{name:'episodes'}">Episode overview</router-link>
                    <a href="https://lw1.at">My other Projects</a>
                    <a href="https://lw1.at/i">Privacy Policy</a>
                </footer>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import Vue from "vue";
import Intro from "@/components/Intro.vue";

export default Vue.extend({
  name: "App",
  components: {
    Intro,
  },
  mounted(): void {
    if (localStorage.getItem("showIntro") !== null) {
      this.showIntro = localStorage.getItem("showIntro") === "true";
    }
  },
  data() {
    return {
      showIntro: true,
    };
  },
  watch: {
    showIntro(value: boolean): void {
      localStorage.setItem("showIntro", value.toString());
    }
  },

});
</script>
