<template>
  <v-tabs v-model="store.selectedAssignment.id" grow show-arrows>
    <v-tab
      v-for="(assignment, index) in allAssignments"
      :key="assignment.id"
      :value="assignment.id"
      @click="changeAssignment(index)"
    >
      {{ assignment.title }}
    </v-tab>
  </v-tabs>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { useAssignmentStore } from '../stores/assignmentStore'
import { Assignment } from '../assets/Commons'

const store = useAssignmentStore() // storeのインスタンスを取得
const allAssignments = ref<Array<Assignment>>([]) // 全課題の情報をローカル管理

// 課題のjsonファイルを取得する(TODO:後でAPIを叩くようにする)
function getWeekFileName(assignmentId: number): string {
  return `static/assignments/week${assignmentId}.json`
}
async function getAssignmentData(assignmentId: number) {
  try {
    const response = await fetch(getWeekFileName(assignmentId))
    if (!response.ok) {
      throw new Error('課題データが読み込めませんでした！')
    }
    const data = await response.json()
    store.selectedAssignment.title = data.title
    store.selectedAssignment.description = data.description
  } catch (error) {
    store.selectedAssignment.title = '未定'
    store.selectedAssignment.description = 'まだ未定です！'
  }
}

// 全Assignmentデータの取得
// TODO : JSONの中身を取得するようにするために、APIを叩くようにする
function generateAssignmentTabs() {
  const numAssignments = 4
  const AssignmentData = []
  for (let i = 1; i <= numAssignments; i++) {
    AssignmentData.push({
      id: i,
      title: `${i}週目`,
      description: `${i}週目の課題です`,
      assignments: []
    })
  }
  allAssignments.value = AssignmentData
}

// storeに現在の課題を保持する
function changeAssignment(index: number) {
  store.selectedAssignment.id = allAssignments.value[index].id
  getAssignmentData(store.selectedAssignment.id)
}

onMounted(() => {
  generateAssignmentTabs()
})
</script>

<style scoped>
.v-tabs {
  justify-content: center;
}
</style>
