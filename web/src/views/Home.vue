<template>
    <div class="home">
        <div class="title">
            <h1>Critical Role Search</h1>
            <span>Find your favourite Critical Role quote!</span>
        </div>
        <transition name="fade">
            <div id="page-mask" v-if="showYtOptIn|| showSeriesSelector"></div>
        </transition>

        <SeriesSelector v-if="showSeriesSelector" :serverData="serverData"></SeriesSelector>
        <div v-if="showYtOptIn" class="ytoptin popup">
            <div>
                <p>This play button allows you to watch the exact timestamp of this quote on YouTube.
                    This means that the YouTube video is loaded on this page and data is sent to YouTube/Google.
                    (<a href="https://lw1.at/i">Privacy Policy</a>)
                </p>
                <p>
                    If you expected this to happen, simply continue and you won't be asked again. Otherwise you can
                    abort or watch this timestamp directly on YouTube.
                </p>
            </div>
            <div class="buttonrow">
                <button class="btn" @click="showYtOptIn=false">abort</button>
                <a class="btn" :href="ytLink" target="youtube" rel="noopener" @click="showYtOptIn=false">YouTube</a>
                <button class="btn" @click="doYtOptIn">continue</button>
            </div>
        </div>
        <div v-if="showYT" class="ytwrapper">
            <button class="btn" @click="closeVideo">Hide</button>
            <youtube :nocookie="true" ref="youtube" @ready="playVideo(false)" :width="ytWidth"></youtube>
        </div>
        <div class="inputlist">
            <span>Search for</span>
            <autocomplete :defaultValue="this.$route.params.keyword" :search="suggest" @submit="handleSubmit"
                          :placeholder="placeholderText"
                          ref="searchInput"></autocomplete>
            <span v-if="!isOneShot">up to episode </span>
            <input v-if="!isOneShot" title="search until episode number"
                   class="form-control" type="number" v-model="episode"
                   min="1" :max="seriesLength">
            <span>in</span>
            <!--                <select title="campaign selection" class="custom-select" v-model="series">-->
            <!--                    <option v-for="series in serverData.series" v-bind:value="series.slug">-->
            <!--                        {{ series.title }}-->
            <!--                    </option>-->
            <!--                </select>-->
            <button class="btn seriesSelectorButton" @click="showSeriesSelector=true">
                {{ seriesTitle }}
            </button>
            <button class="btn submit" @click="handleSubmit(undefined)">
                !
            </button>

        </div>
        <b-alert v-if="error" show :variant="error.status">{{ error.message }}</b-alert>
        <div class="entry" v-for="result in searchResult">
            <div class="title">
                <div>{{ formatTimestamp(firstLine(result).starttime) }} {{ episodeName(firstLine(result)) }}</div>
                <div class="buttons">
                    <router-link :to="transcriptLink(result)" class="btn" target="_blank" v-b-tooltip
                                 title="Open this line in Transcript">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                             class="bi bi-blockquote-left" viewBox="0 0 16 16">
                            <path d="M2.5 3a.5.5 0 0 0 0 1h11a.5.5 0 0 0 0-1h-11zm5 3a.5.5 0 0 0 0 1h6a.5.5 0 0 0 0-1h-6zm0 3a.5.5 0 0 0 0 1h6a.5.5 0 0 0 0-1h-6zm-5 3a.5.5 0 0 0 0 1h11a.5.5 0 0 0 0-1h-11zm.79-5.373c.112-.078.26-.17.444-.275L3.524 6c-.122.074-.272.17-.452.287-.18.117-.35.26-.51.428a2.425 2.425 0 0 0-.398.562c-.11.207-.164.438-.164.692 0 .36.072.65.217.873.144.219.385.328.72.328.215 0 .383-.07.504-.211a.697.697 0 0 0 .188-.463c0-.23-.07-.404-.211-.521-.137-.121-.326-.182-.568-.182h-.282c.024-.203.065-.37.123-.498a1.38 1.38 0 0 1 .252-.37 1.94 1.94 0 0 1 .346-.298zm2.167 0c.113-.078.262-.17.445-.275L5.692 6c-.122.074-.272.17-.452.287-.18.117-.35.26-.51.428a2.425 2.425 0 0 0-.398.562c-.11.207-.164.438-.164.692 0 .36.072.65.217.873.144.219.385.328.72.328.215 0 .383-.07.504-.211a.697.697 0 0 0 .188-.463c0-.23-.07-.404-.211-.521-.137-.121-.326-.182-.568-.182h-.282a1.75 1.75 0 0 1 .118-.492c.058-.13.144-.254.257-.375a1.94 1.94 0 0 1 .346-.3z"/>
                        </svg>
                    </router-link>
                    <button class="btn" @click="playVideo(result)" title="Watch line on YouTube" v-b-tooltip>
                        <b-icon-play-fill></b-icon-play-fill>
                    </button>
                    <button class="btn" v-if="result.offset<10" @click="expand(result)" title="Load more context"
                            v-b-tooltip>
                        +
                    </button>
                </div>
            </div>
            <p :class="{line:true,note:line.isnote,meta:line.ismeta}" :style="{borderLeftColor:getColor(line)}"
               v-for="line in result.lines" :key="line.id">
                <span v-if="line.person" class="person">{{ line.person.name }}: </span><span
                    v-html="line.text"></span>
            </p>
        </div>
        <!--            <details>-->
        <!--                <summary>Raw Data</summary>-->
        <!--                <pre>{{ searchResult }}</pre>-->
        <!--            </details>-->

    </div>
</template>

<script lang="ts">
import Vue from "vue";
// @ts-ignore
import Autocomplete from "@trevoreyre/autocomplete-vue";
// import "@trevoreyre/autocomplete-vue/dist/style.css";
import {Line, Result, SeriesData, ServerData, ServerMessage} from "@/interfaces";
import {BAlert, BIcon, BIconPlayFill} from "bootstrap-vue";
// @ts-ignore
import VueYoutube from "vue-youtube";
import debounce from "lodash-es/debounce";
import {Location} from "vue-router";
import {baseURL} from "@/utils";
import SeriesSelector from "@/components/SeriesSelector.vue";
import Intro from "@/components/Intro.vue";

Vue.use(VueYoutube);


export default Vue.extend({
  name: "home",
  components: {
    Intro,
    SeriesSelector,
    Autocomplete,
    BAlert,
    BIcon,
    BIconPlayFill,
  },
  data() {
    return {
      serverData: {series: []} as ServerData,
      searchResult: [] as Result[],
      episode: this.$route.params.episode,
      error: undefined as ServerMessage | undefined,
      ytOptIn: false,
      showYtOptIn: false,
      ytVideoID: undefined as string | undefined,
      showYT: false,
      ytResult: undefined as Result | undefined,
      ytWidth: 640,
      showSeriesSelector: false,
      placeholderText: "",
      placeholderFullText: "",
      placeholderTimeout: 0,
      placeholderInterval: 0
    };
  },
  created() {
    fetch(baseURL + "series")
      .then((response) => response.json())
      .then((data: ServerData) => {
        this.serverData = data;
      });
    this.placeholderTimeout = setTimeout(this.startTyping, 7 * 1000);
  },
  beforeDestroy() {
    clearTimeout(this.placeholderTimeout);
  },
  mounted(): void {
    if (localStorage.getItem("ytOptIn") !== null) {
      this.ytOptIn = localStorage.getItem("ytOptIn") === "true";
    }
    if (this.episode == null) {
      this.episode = "10";
    }
    if (this) {
      document.title = "CR Search";
    }
    if (this.$route.params.keyword) {
      this.search();
    }
    const max = 640;
    this.ytWidth = (window.innerWidth < max ? window.innerWidth : max) - 2 * 2;
  },
  methods: {
    suggest(input: string) {
      const url = baseURL
        + "suggest?query=" + input
        + "&until=" + this.episode
        + "&series=" + this.$route.params.series;

      return new Promise((resolve) => {
        if (input.length < 1) {
          return resolve([]);
        }
        fetch(url)
          .then((response) => response.json())
          .then((data: string[]) => {
            resolve(data);
          });
      });
    },
    handleSubmit(result: string) {
      // @ts-ignore
      const newKeyword = result || this.$refs.searchInput.value;
      if (newKeyword === "" && this.placeholderFullText) {
        // @ts-ignore
        this.$refs.searchInput.value = this.placeholderFullText;
        this.handleSubmit(this.placeholderFullText);
        return;
      }
      this.$router.push({params: {...this.$route.params, keyword: newKeyword}});

    },
    search(): void {
      if (!this.$route.params.keyword) {
        return;
      }
      const url = baseURL
        + "search?query=" + this.$route.params.keyword
        + "&until=" + this.episode
        + "&series=" + this.$route.params.series;

      fetch(url)
        .then((response) => response.json())
        .then((data) => {
          if (data.status) {
            this.error = data;
            this.searchResult = [];
          } else {
            this.error = undefined;
            this.searchResult = data;
          }
        });
    },
    expand(result: Result) {
      const offset = result.offset ? result.offset : 1;
      const url = baseURL + "expand?centerID=" + result.centerID + "&offset=" + offset;

      fetch(url)
        .then((response) => response.json())
        .then((data: Line[]) => {

          this.searchResult[result.resultID].lines.push(...data);
          this.searchResult[result.resultID].lines.sort((a, b) => a.order - b.order);
          this.searchResult[result.resultID].offset = offset + 1;
        });

    },
    firstLine(result: Result): Line {
      return result.lines[0];
    },
    episodeName(line: Line): string {
      if (line.episode.series.is_campaign) {
        return `Episode ${line.episode.episode_number}: ${line.episode.pretty_title}`;
      }
      return line.episode.pretty_title;
    },
    formatTimestamp(ts: number) {
      return new Date(ts).toISOString().substr(11, 8);
    },
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
    doYtOptIn() {
      this.showYtOptIn = false;
      this.ytOptIn = true;
      this.playVideo(undefined);
    },
    playVideo(result: Result | undefined): void {
      if (!this.ytOptIn) {
        this.ytResult = result;
        this.showYtOptIn = true;
        return;
      }
      if (!result && this.ytResult) {
        result = this.ytResult;
      }
      if (!result) {
        return;
      }
      const firstLine = this.firstLine(result);
      const newYtVideoID = firstLine.episode.youtube_id;
      if (!this.$refs.youtube) {
        this.showYT = true;
        this.ytResult = result;
      } else {
        // @ts-ignore
        const player = this.$refs.youtube.player;
        if (firstLine) {
          if (this.ytVideoID === newYtVideoID) {
            player.seekTo(firstLine.starttime / 1000);
          } else {
            player.loadVideoById(
              newYtVideoID,
              firstLine.starttime / 1000,
              firstLine.endtime / 1000
            );
            this.ytVideoID = newYtVideoID;
          }
        }
      }
    },
    closeVideo(): void {
      this.showYT = false;
      this.ytVideoID = undefined;
      this.ytResult = undefined;
    },
    startTyping(): void {
      // @ts-ignore
      if (this.$refs.searchInput.value !== "") {
        this.placeholderTimeout = setTimeout(this.startTyping, 5000);
        return;
      }
      const url = baseURL
        + "suggestion"
        + "?until=" + this.episode
        + "&series=" + this.$route.params.series;

      fetch(url)
        .then((response) => {
          if (!response.ok) {
            throw new Error();
          }
          return response.text();
        })
        .then((data) => {
          this.placeholderFullText = data;
          clearTimeout(this.placeholderTimeout);
          this.placeholderText = "";
          this.typing(0);
        })
        .catch((error) => {
          this.placeholderTimeout = setTimeout(this.startTyping, 5000);
        });

    },
    typing(index: number): void {
      if (index === this.placeholderFullText.length) {
        this.placeholderTimeout = setTimeout(this.untype, 5000);
        return;
      }
      this.placeholderText += this.placeholderFullText[index];
      const offset = Math.random() * 80 - 40;
      this.placeholderTimeout = setTimeout(this.typing, 70 + offset, index + 1);
    },
    untype(): void {
      if (this.placeholderText.length === 0) {
        this.placeholderTimeout = setTimeout(this.startTyping, 5000);
        return;
      }
      this.placeholderText = this.placeholderText.slice(0, -1);
      const offset = Math.random() * 40 - 20;
      this.placeholderTimeout = setTimeout(this.untype, 35 + offset);
    },
    transcriptLink(result: Result): Location {
      const firstline = this.firstLine(result);
      const episode = firstline.episode;
      return {
        name: "transcript",
        params: {
          episodeNr: episode.episode_number.toString(),
          series: episode.series.slug
        },
        hash: "#" + firstline.starttime
      };
    }
  },
  computed: {
    ytLink(): string {
      if (!this.ytResult) {
        return "";
      }
      const firstline = this.firstLine(this.ytResult);
      const starttime = firstline.starttime / 1000;
      const id = firstline.episode.youtube_id;
      const min = Math.floor(starttime / 60);
      const sec = Math.floor(starttime % 60);
      return `https://www.youtube.com/watch?v=${id}&t=${min}m${sec}s`;
    },
    seriesFromSlug(): SeriesData | undefined {
      if (!this.$route.params.series) {
        return undefined;
      }
      return this.serverData.series.find((series) => {
        return series.slug === this.$route.params.series;
      });
    },
    seriesTitle(): string {
      const series = this.seriesFromSlug;
      if (series) {
        return series.title;
      } else {
        return this.$route.params.series;
      }
    },
    seriesLength(): number {
      const series = this.seriesFromSlug;
      if (series) {
        return series.length;
      }
      return 300;
    },
    isOneShot(): boolean {
      return this.episode === "-";
    }
  },
  watch: {
    episode: debounce(function(val: number): void {
      // @ts-ignore
      this.$router.push({params: {...this.$route.params, episode: val}});
    }, 300),
    "$route.params.keyword"(val: string): void {
      // @ts-ignore
      this.$refs.searchInput.value = this.$route.params.keyword;
    },
    "$route.params"(val) {
      // this.series = this.$route.params.series;
      this.showSeriesSelector = false;
      this.search();
    },
    ytOptIn(value: boolean): void {
      localStorage.setItem("ytOption", value.toString());
    },
  },
});
</script>
