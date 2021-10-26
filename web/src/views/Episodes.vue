<template>
    <div class="text-page">
        <h1>Episode Overview</h1>
        <div v-for="series in series_data" :key="series.meta.id" class="episode-table">
            <h2 :id="seriesID(series.meta)">{{ series.meta.title }}</h2>
            <table>
                <thead>
                <tr>
                    <th>Title</th>
                    <th></th>
                    <th>Episode</th>
                    <th>Video</th>
                    <th>Upload Date</th>
                    <th>Subtitles available and fetched</th>
                    <th>Subtitles imported in search</th>
                    <th>Phrases imported for search suggestions</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="episode in series.episodes" :key="episode.id">
                    <td><a :href="youtubeLink(episode)" target="youtube" rel="noopener">
                        {{ episode.pretty_title }}
                    </a>
                    </td>
                    <td>
                        <router-link class="btn" :to="transcriptLink(episode,series.meta)">T</router-link>
                    </td>
                    <td>{{ episode.episode_number }}</td>
                    <td>{{ episode.video_number }}</td>
                    <td>{{ episode.upload_date }}</td>
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
    </div>
</template>

<script lang="ts">
import Vue from "vue";
import {EpisodeDetailed, Series, SeriesData} from "@/interfaces";
import {baseURL} from "@/utils";
import CheckMark from "@/components/CheckMark.vue";
import {Location} from "vue-router";

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
    document.title = "Episode Overview | CR Search";
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
    },
    transcriptLink(episode: EpisodeDetailed, series: Series): Location {
      return {
        name: "transcript",
        params: {
          episodeNr: episode.episode_number.toString(),
          series: series.slug
        }
      };
    }
  }
});
</script>
