<template>
    <div class="showIntro popup">
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
            <button class="btn" @click="closeIntro">Close</button>
        </div>
    </div>
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
  name: "Intro",
  methods: {
    closeIntro() {
      // @ts-ignore
      this.$parent.showIntro = false;
    }
  }
});
</script>
