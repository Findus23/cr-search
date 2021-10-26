<template>
    <div class="seriesSelector popup">
        <h1>Select Series</h1>
        <form class="form-inline">
            <div class="form-check mb-2 mr-sm-2">
                <input class="form-check-input" type="checkbox" id="onlyCampaigns" v-model="onlyCampaigns">
                <label class="form-check-label" for="onlyCampaigns">show only campaigns</label>
            </div>
            <div class="form-check mb-2 mr-sm-2">
                <input class="form-check-input" type="checkbox" id="showOneShots" v-model="showOneShots">
                <label class="form-check-label" for="showOneShots">show One-Shots</label>
            </div>
            <input class="form-control" type="search" id="search" v-model="search" placeholder="search">
        </form>
        <transition-group name="flip-list" class="seriesList" tag="div">
            <router-link class="series" v-for="series in sortedSeries" :to="createLink(series)"
                         @click.native="selectSeries" :key="series.id">
                <div>{{ series.title }}</div>
                <img :src="'https://cr-search.lw1.at/static/'+series.slug+'.webp'">
            </router-link>
        </transition-group>
    </div>
</template>

<script lang="ts">
import Vue, {PropType} from "vue";
import {SeriesData, ServerData} from "@/interfaces";

export default Vue.extend({
  name: "SeriesSelector",
  props: {
    serverData: Object as PropType<ServerData>
  },
  data() {
    return {
      onlyCampaigns: false,
      showOneShots: true,
      search: ""
    };
  },
  computed: {
    sortedSeries(): SeriesData[] {
      return this.serverData.series.filter((series) => {
        if (!series.is_campaign && this.onlyCampaigns) {
          return false;
        }
        if ((series.length === 1 && !series.is_campaign) && !this.showOneShots) {
          return false;
        }
        return this.search === "" || series.title.toLowerCase().includes(this.search.toLowerCase());

      }).sort((a, b) => {
        return b.last_upload.localeCompare(a.last_upload);
      });
    }
  },
  methods: {
    selectSeries(): void {
      // @ts-ignore
      this.$parent.showSeriesSelector = false;
    },
    createLink(series: SeriesData) {

      const episode = (series.length === 1 && !series.is_campaign) ? "-" : 10;
      return {
        name: "search",
        params: {series: series.slug, episode}
      };
    }
  }
});
</script>
