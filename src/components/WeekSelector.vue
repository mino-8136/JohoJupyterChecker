<template>
  <v-tabs v-model:active="selectedWeekIndex" grow>
    <v-tab v-for="(week, index) in weeks" :key="week" @click="changeWeek(index)">
      {{ week }}
    </v-tab>
  </v-tabs>
</template>

<script setup lang="ts">
import { ref, defineEmits } from "vue";

const emit = defineEmits(["selected-week"]); // 親に週情報を返すためのemit関数
const selectedWeekIndex = ref(0); // 週の選択状態を管理
const weeks = ['1週目', '2週目', '3週目', '4週目'];
const changeWeek = (index: number) => {
  selectedWeekIndex.value = index;
  
  // 親に週情報を返す
  emit("selected-week", selectedWeekIndex.value)
};
</script>

<style scoped>
.v-tabs {
  justify-content: center;
}
</style>
