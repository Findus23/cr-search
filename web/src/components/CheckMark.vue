<template>
    <span class="checkmark">
        <span v-if="status" class="value true">
            &checkmark;
        </span>
        <span v-else class="value false">
            &cross;
        </span>
    </span>
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
  name: "CheckMark",
  props: {
    status: Boolean,
  }
});
</script>
