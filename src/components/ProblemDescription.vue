<template>
  <h3 class="my-4">{{ weekData.title }}</h3>
  <p>{{ weekData.description }}</p>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const prop = defineProps<{
  week: number
}>()

// 画面に表示するための関数
const weekData = ref({
  title: '未定',
  description: 'まだ未定です！'
})

function getWeekFileName(week: number): string {
  return `static/problems/week${week + 1}.json`
}

function displayWeekData(week: number) {
  fetch(getWeekFileName(week))
    .then((response) => {
      if (!response.ok) {
        throw new Error('課題データが読み込めませんでした！')
      }
      return response.json()
    })
    .then((data) => {
      weekData.value.title = data.title
      weekData.value.description = data.description
    })
    .catch((error) => {
      weekData.value.title = '未定',
      weekData.value.description = 'まだ未定です！'
    })
}

onMounted(() => {
  displayWeekData(prop.week)
})

defineExpose({
  displayWeekData
})

</script>
