<template>
    <div id="contentwrapper">
        <div class="home">
            <div class="title">
                <h1>Critical Role Search</h1>
                <span>Find your favourite Critical Role quote!</span>
            </div>
            <transition name="fade">
                <div id="page-mask" v-if="showIntro || showYtOptIn"></div>
            </transition>
            <div v-if="showIntro" class="showIntro popup">
                <div class="title"><h1>Critical Role Search</h1></div>
                <div>
                    <p>
                        This website uses subtitles to allow a full text search through all
                        <a href="https://critrole.com/">Critical Role</a> episodes.
                    </p>
                    <p>Subtitles for Campaign 1 and Campaign 2 up to Episode 54 by the
                        <a href="https://crtranscript.tumblr.com/" target="_blank" rel="noopener">CR Transcript
                            Team</a>,
                        all other subtitles are by the Critical Role team.
                    </p>
                    <p>
                        This website is licensed under the
                        <a href="https://www.gnu.org/licenses/gpl-3.0.en.html">GPL-3.0</a>.
                        You can find the source <a href="#">here</a>.
                    </p>
                    <dl>
                        <dt>Fonts</dt>
                        <dd>
                            <a href="https://github.com/jonathonf/solbera-dnd-fonts" target="_blank" rel="noopener">
                                by Solbera and Ryrok
                            </a> (CC BY-SA 4.0)
                        </dd>
                        <dt>Design</dt>
                        <dd>
                            Inspired by
                            <a href="https://homebrewery.naturalcrit.com/" target="_blank" rel="noopener">
                                The Homebrewery
                            </a>
                            (MIT License)
                        </dd>
                    </dl>
                </div>
                <div class="buttonrow">
                    <button class="btn" @click="showIntro=false">Close</button>
                </div>
            </div>
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
                <autocomplete :defaultValue="keyword" :search="suggest" @submit="handleSubmit"
                              ref="searchInput"></autocomplete>
                <span>up to episode </span>
                <input title="search until episode number"
                       class="form-control" type="number" v-model="episode"
                       min="1" max="300">
                <span>in</span>
                <select title="campaign selection" class="custom-select" v-model="series">
                    <option v-for="series in serverData.series" v-bind:value="series.id">
                        {{ series.title }}
                    </option>
                </select>
            </div>
            <b-alert v-if="error" show :variant="error.status">{{ error.message }}</b-alert>
            <div class="entry" v-for="result in searchResult">
                <div class="title">
                    <div>{{ formatTimestamp(firstLine(result).starttime) }} {{ episodeName(firstLine(result)) }}</div>
                    <div class="buttons">
                        <button class="btn" @click="playVideo(result)" title="View video on YouTube">
                            <b-icon-play-fill></b-icon-play-fill>
                        </button>
                        <button class="btn" v-if="result.offset<10" @click="expand(result)" title="Load more context">
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
            <details>
                <summary>Raw Data</summary>
                <pre>{{ searchResult }}</pre>
            </details>

        </div>
        <footer>
            <button @click="showIntro=true" class="btn btn-link">About this website</button>
            <a href="https://lw1.at">My other Projects</a>
            <a href="https://lw1.at/i">Privacy Policy</a>
        </footer>
    </div>
</template>

<script lang="ts">
import Vue from "vue";
// @ts-ignore
import Autocomplete from "@trevoreyre/autocomplete-vue";
// import "@trevoreyre/autocomplete-vue/dist/style.css";
import {Line, Result, ServerData, ServerMessage} from "@/interfaces";
import {BAlert, BIcon, BIconPlayFill} from "bootstrap-vue";
// @ts-ignore
import VueYoutube from "vue-youtube";
import debounce from "lodash-es/debounce";

import {baseURL} from "@/utils";

Vue.use(VueYoutube);


export default Vue.extend({
  name: "home",
  components: {
    Autocomplete,
    BAlert,
    BIcon,
    BIconPlayFill,
  },
  data() {
    return {
      serverData: {"series": []} as ServerData,
      searchResult: [] as Result[],
      keyword: this.$route.params.keyword,
      series: this.$route.params.series,
      episode: this.$route.params.episode,
      error: undefined as ServerMessage | undefined,
      ytOptIn: false,
      showYtOptIn: false,
      ytVideoID: undefined as string | undefined,
      showYT: false,
      ytResult: undefined as Result | undefined,
      ytWidth: 640,
      showIntro: true
    };
  },
  mounted(): void {
    if (localStorage.showIntro) {
      this.showIntro = localStorage.showIntro;
    }
    if (localStorage.ytOptIn) {
      this.ytOptIn = localStorage.ytOptIn;
    }
    if (this.series == null) {
      this.series = "2";
    }
    if (this.episode == null) {
      this.episode = "10";
    }
    if (this) {
      document.title = "CR Search";
    }
    if (this.keyword) {
      this.search();
    }
    const max = 640;
    this.ytWidth = (window.innerWidth < max ? window.innerWidth : max) - 2 * 2;
    fetch(baseURL + "series")
      .then((response) => response.json())
      .then((data: ServerData) => {
        this.serverData = data;
      });

  },
  methods: {
    suggest(input: string) {
      const url = baseURL + "suggest?query=" + input + "&until=" + this.episode + "&series=" + this.series;

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
      this.keyword = result || this.$refs.searchInput.value;
    },
    search(): void {
      if (!this.keyword) {
        return;
      }
      const url = baseURL + "search?query=" + this.keyword + "&until=" + this.episode + "&series=" + this.series;

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
    }
  },
  watch: {
    episode: debounce(function(val: number): void {
      // @ts-ignore
      this.$router.replace({params: {...this.$route.params, episode: val}});
    }, 300),
    series(val: string): void {
      this.$router.replace({params: {...this.$route.params, series: val}});
    },
    keyword(val: string): void {
      this.$router.replace({params: {...this.$route.params, keyword: val}});
    },
    "$route.params"(val) {
      this.search();
    },
    ytOptIn(value: boolean): void {
      localStorage.ytOptIn = value;
    }
  },
});
</script>
