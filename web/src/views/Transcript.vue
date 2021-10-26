<template>
    <div id="contentwrapper" class="text-page">
        <h1>{{ episode.pretty_title }}</h1>
        <p>
            <router-link :to="{name:'home'}">Back to the Homepage</router-link>
        </p>

        <blockquote>
            <strong>Note:</strong> This transcript-view is a work in progress and currently only shows very basic data.
            One day it might allow to jump to the position of a line in the Youtube video like on the main page.
        </blockquote>

        <p :class="{line:true,note:line.isnote,meta:line.ismeta,highlighted:$route.hash.slice(1)===line.starttime.toString()}"
           :style="{borderLeftColor:getColor(line)}"
           v-for="line in lines" :key="line.id" :id="line.starttime">
            <span v-if="line.person" class="person">{{ line.person.name }}: </span><span
                v-html="line.text"></span>
        </p>
    </div>
</template>

<script lang="ts">
import Vue from "vue";
import {Episode, Line, TranscriptData} from "@/interfaces";
import {baseURL} from "@/utils";
import CheckMark from "@/components/CheckMark.vue";

export default Vue.extend({
  name: "Transcript",
  props: {
    episodeNr: String,
    series: String
  },
  components: {
    CheckMark
  },
  data() {
    return {
      lines: [] as Line[],
      episode: {} as Episode,
      loaded: false
    };
  },
  mounted() {
    console.log(this.episodeNr);
    fetch(baseURL + "transcript?episode=" + this.episodeNr + "&series=" + this.series)
      .then((response) => response.json())
      .then((data: TranscriptData) => {
        this.episode = data.episode;
        this.lines = data.lines;
        this.loaded = true;
        const hash = this.$route.hash;
        if (hash) {
          Vue.nextTick(function() {
            document.getElementById(hash.slice(1))?.scrollIntoView({
              behavior: "smooth",
            });
          });
        }
      });
  },
  methods: {
    getColor(line: Line): string {
      if (line.ismeta) {
        return "pink";
      } else if (line.isnote) {
        return "purple";
      }
      if (line.person) {
        return line.person.color;
      }
      return "white";
    },

  }
});
</script>
