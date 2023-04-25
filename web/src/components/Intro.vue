<template>
    <div class="showIntro popup">
        <div class="title"><h1>Critical Role Search</h1></div>
        <div>
            <p>
                This Website uses subtitles to allow you to search through the text of all<sup>1</sup> episodes of
                <a href="https://critrole.com/">Critical Role</a>.
            </p>
            <p>In addition to a plain search there is a text completion from common phrases, a upper episode limit
                selector to avoid getting spoilered by something that occurs in a later episode<sup>2</sup> and an
                experimental transcript view.</p>
            <p>If you have any feedback, ideas for improvements or bugs, feel free to contact me at
                <a href="mailto:cr@lw1.at">cr@lw1.at</a> or <a href="https://twitter.com/lw1_at">on Twitter</a>.</p>
            <p>You can learn more about this website <a href="https://lw1.at/en/cr-search/">here</a>.</p>
            <div class="footnote-list">
                <ol>
                    <li>all episodes with manually created subtitles (including Shows and One-Shots)</li>
                    <li>this also affects search suggestions</li>
                </ol>
            </div>
            <button class="btn btn-primary to-website-button" @click="closeIntro">Go to the Website</button>

            <hr>
            <p>Subtitles for Campaign 1 and Campaign 2 up to Episode 54 by the
                <a href="https://crtranscript.tumblr.com/" target="_blank" rel="noopener">
                    CR Transcript Team
                </a>,
                all other subtitles are by the Critical Role team.
            </p>
            <p>
                This website is licensed under the
                <a href="https://www.gnu.org/licenses/gpl-3.0.en.html">GPL-3.0</a>.
                You can find the source code for both the backend doing the search and the frontend visualising the
                results <a href="https://github.com/Findus23/cr-search">here</a>.
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
            <button class="btn btn-primary" @click="closeIntro">Close</button>
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
