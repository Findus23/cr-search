<template>
    <div class="seriesSelector popup">
        <h1>Select Series</h1>
        <input type="checkbox" id="onlyCampaigns" v-model="onlyCampaigns">
        <label for="onlyCampaigns">show only campaigns</label>
        <input type="checkbox" id="showOneShots" v-model="showOneShots">
        <label for="showOneShots">show One-Shots</label>
        <input type="search" id="search" v-model="search">
        <label for="search">search</label>

        <transition-group name="flip-list" class="seriesList" tag="div">
            <div class="series" v-for="series in sortedSeries" @click="selectSeries(series)" :key="series.id">
                <span>{{ series.title }}</span>
                <img :src="'http://127.0.0.1:5000/static/'+series.slug+'.webp'">
            </div>
        </transition-group>
    </div>
</template>

<script lang="ts">
import Vue, {PropType} from "vue";
import {Series, SeriesData, ServerData} from "@/interfaces";

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
      console.log(this.search);
      return this.serverData.series.filter((series) => {
        console.log(series.title.includes(this.search))
        if (!series.is_campaign && this.onlyCampaigns) {
          return false;
        }
        if (series.length === 1 && !this.showOneShots) {
          return false;
        }
        return this.search === "" || series.title.toLowerCase().includes(this.search.toLowerCase());

      }).sort((a, b) => {
        return b.last_upload.localeCompare(a.last_upload);
      });
    }
  },
  methods: {
    selectSeries(series: SeriesData): void {
      // @ts-ignore
      this.$parent.selectSeries(series);
    }
  }
});
</script>
