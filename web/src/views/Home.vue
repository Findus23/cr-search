<template>
    <div class="home">
        <div class="title">
            <h1>Critical Role Search</h1>
            <span>Find your favourite Critical Role quote!</span>
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
            <select title="campaign selection" class="custom-select" v-model="season">
                <option value="1">Campaign 1</option>
                <option value="2">Campaign 2</option>
            </select>
        </div>
        <b-alert v-if="error" show :variant="error.status">{{error.message}}</b-alert>
        <div class="entry" v-for="result in searchResult">
            <div class="title">
                <div>{{episodeName(firstLine(result))}} {{formatTimestamp(firstLine(result).starttime)}}</div>
                <div class="buttons">
                    <button class="btn" @click="playVideo(result)">
                        <b-icon-play-fill></b-icon-play-fill>
                    </button>
                    <button class="btn" v-if="result.offset<10" @click="expand(result)">
                        +
                    </button>
                </div>
            </div>
            <p :class="{line:true,note:line.isnote|line.ismeta}" :style="{borderLeftColor:getColor(line)}"
               v-for="line in result.lines" :key="line.id">
                <span v-if="line.person" class="person">{{line.person.name}}: </span><span v-html="line.text"></span>
            </p>
        </div>
        <pre>{{searchResult}}</pre>

    </div>
</template>

<script lang="ts">
  import Vue from "vue";
  // @ts-ignore
  import Autocomplete from "@trevoreyre/autocomplete-vue";
  // import "@trevoreyre/autocomplete-vue/dist/style.css";
  import {Line, Result, ServerMessage} from "@/interfaces";
  import {BAlert, BIcon, BIconPlayFill} from "bootstrap-vue";
  // @ts-ignore
  import VueYoutube from "vue-youtube";
  import {debounce} from "lodash";

  Vue.use(VueYoutube);

  const baseURL = (process.env.NODE_ENV === "production") ? "/api/" : "http://127.0.0.1:5000/api/";

  export default Vue.extend({
    name: "home",
    components: {
      Autocomplete,
      BAlert,
      BIcon,
      BIconPlayFill,
    },
    // props: {
    //   keyword: String,
    //   season: String,
    //   episode: String
    // },
    data() {
      return {
        searchResult: [] as Result[],
        keyword: this.$route.params.keyword,
        season: this.$route.params.season,
        episode: this.$route.params.episode,
        error: undefined as ServerMessage | undefined,
        ytVideoID: undefined as string | undefined,
        showYT: false,
        ytResult: undefined as Result | undefined,
        ytWidth: 640
      };
    },
    mounted(): void {
      document.title = "CR Search";
      if (this.keyword) {
        this.search();
      }
      const max = 640;
      this.ytWidth = (window.innerWidth < max ? window.innerWidth : max) - 2 * 2;
    },
    methods: {
      suggest(input: string) {
        const url = baseURL + "suggest?query=" + input + "&until=" + this.episode + "&season=" + this.season;

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
        const url = baseURL + "search?query=" + this.keyword + "&until=" + this.episode + "&season=" + this.season;

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
        return `C${line.episode.season}E${line.episode.episode_number}`;
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
        return line.person.color;
      },
      playVideo(result: Result): void {
        if (!result && this.ytResult) {
          result = this.ytResult;
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
    watch: {
      episode: debounce(function(val: number): void {
        // @ts-ignore
        this.$router.replace({params: {...this.$route.params, episode: val}});
      }, 300),
      season(val: string): void {
        this.$router.replace({params: {...this.$route.params, season: val}});
      },
      keyword(val: string): void {
        this.$router.replace({params: {...this.$route.params, keyword: val}});
      },
      "$route.params": function(val) {
        this.search();
      }
    },
  });
</script>
