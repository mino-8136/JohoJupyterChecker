<template>
  <v-tabs v-model:active="selectedWeekIndex" grow>
    <v-tab v-for="(week, index) in weeks" :key="week" @click="changeWeek(index)">
      {{ week }}
    </v-tab>
  </v-tabs>
</template>

<script setup lang="ts">
import { ref } from "vue";

const selectedWeekIndex = ref(0);
const weeks = ['1週目', '2週目', '3週目', '4週目'];
const changeWeek = (index: number) => {
  selectedWeekIndex.value = index;
  const week = weeks[index];
  // JSONファイルを読み込む処理を追加する
  console.log(`Selected week: ${week}`);
};
</script>

<style scoped>
.v-tabs {
  justify-content: center;
}
</style>
