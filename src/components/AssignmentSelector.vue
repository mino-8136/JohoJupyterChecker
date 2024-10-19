<template>
  <v-tabs v-model="selectedAssignmentId" grow show-arrows>
    <v-tab
      v-for="(assignment, index) in allAssignments"
      :key="assignment.id"
      :value="assignment.id"
      style="text-transform: none"
      @click="changeAssignment(index)"
      show-arrows
    >
      {{ assignment.title }}
    </v-tab>
  </v-tabs>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useAssignmentStore } from '../stores/assignmentStore'
import { Assignment } from './utils/Commons'

const store = useAssignmentStore()
const allAssignments = ref<Array<Assignment>>([]) // 全課題の情報をローカル管理
const selectedAssignmentId = ref<number | null>(null) // 選択された課題のIDをローカルに管理

// 指定コース内の全Assignmentデータを取得する
async function getAllAssignments(course: string | null) {
  try {
    const response = await fetch('http://localhost:5000/api/assignments', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ course })
    })
    if (!response.ok) {
      throw new Error('課題データの取得に失敗しました')
    }

    const data = await response.json()
    allAssignments.value = data
  } catch (e) {
    console.error(e)
  }
}

// storeに現在の課題を保持すると同時に、選択された課題のIDをローカルに保持する
function changeAssignment(index: number) {
  store.selectedAssignment = allAssignments.value[index]
  selectedAssignmentId.value = allAssignments.value[index].id
}

watch(
  () => store.selectedCourse,
  async (newCourse) => {
    if (newCourse) {
      await getAllAssignments(newCourse)
      changeAssignment(0) // コースが変更されたら最初の課題を選択
    }
  }
)

onMounted(async () => {
  // 課題一覧の取得
  await getAllAssignments(store.selectedCourse)
  changeAssignment(0) // 初期状態で最初の課題を選択
})
</script>

<style scoped>
.v-tabs {
  justify-content: center;
}
</style>
