<template>
    <div id="contentwrapper" class="text-page">
        <h1>Episode Overview</h1>
<!--        <div v-for="series in series_data">-->
<!--            <a :href="seriesID(series.meta,true)">{{ series.meta.title }}</a>-->
<!--        </div>-->


        <div v-for="series in series_data" :key="series.meta.id" class="episode-table">
            <h2 :id="seriesID(series.meta)">{{ series.meta.title }}</h2>
            <table>
                <thead>
                <tr>
                    <th>Title</th>
                    <th>Episode</th>
                    <th>Video</th>
                    <th>Subtitles available and fetched</th>
                    <th>Subtitles imported in search</th>
                    <th>Phrases imported for search suggestions</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="episode in series.episodes" :key="episode.id">
                    <td><a :href="youtubeLink(episode)" target="youtube" rel="noopener">
                        {{ episode.title }}
                    </a>
                    </td>
                    <td>{{ episode.episode_number }}</td>
                    <td>{{ episode.video_number }}</td>
                    <td class="text-center">
                        <CheckMark :status="episode.downloaded"></CheckMark>
                    </td>
                    <td class="text-center">
                        <CheckMark :status="episode.text_imported"></CheckMark>
                    </td>
                    <td class="text-center">
                        <CheckMark :status="episode.phrases_imported"></CheckMark>
                    </td>
                </tr>
                </tbody>
            </table>
        </div>
        <pre>{{ series_data }}</pre>
    </div>
</template>

<script lang="ts">
import Vue from "vue";
import {EpisodeDetailed, Series, SeriesData} from "@/interfaces";
import {baseURL} from "@/utils";
import CheckMark from "@/components/CheckMark.vue";

export default Vue.extend({
  name: "Episodes",
  components: {
    CheckMark
  },
  data() {
    return {
      series_data: [] as SeriesData[]
    };
  },
  mounted() {
    fetch(baseURL + "episodes")
      .then((response) => response.json())
      .then((data: SeriesData[]) => {
        this.series_data = data;
      });
  },
  methods: {
    youtubeLink(episode: EpisodeDetailed) {
      return `https://www.youtube.com/watch?v=${episode.youtube_id}`;
    },
    episodeID(episode: EpisodeDetailed, withHash: boolean) {
      return (withHash ? "#" : "") + `episode-${episode.id}`;
    },
    seriesID(series: Series, withHash: boolean) {
      return (withHash ? "#" : "") + `series-${series.id}`;
    }
  }
});
</script>
