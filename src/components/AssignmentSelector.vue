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
import { ref } from 'vue'
import { useAssignmentStore } from '../stores/assignmentStore'
import { Assignment } from './utils/Commons'

const store = useAssignmentStore()
const allAssignments = ref<Array<Assignment>>([]) // 全課題の情報をローカル管理(storeしない)
const selectedAssignmentId = ref<number | null>(null) // 選択された課題のIDをローカルに管理

// store.allCoursesのキーの型を定義する
interface AllCoursesJSON {
  [key: string]: any
}
interface AllAssignmentsJSON {
  url: string
}

// 指定コース内の全Assignmentデータを取得する(親コンポーネントから呼び出し)
async function getAllAssignments(course: string) {
  // 既に読み込まれている課題データを初期化
  allAssignments.value = []
  store.initiateSelectedAssignment()

  // store.allCoursesJSONから指定コース名をもとに、課題データを取得
  const allCourses: AllCoursesJSON = store.allCoursesJSON
  allCourses[course].assignments.forEach(async (assignment: AllAssignmentsJSON) => {
    try {
      // 指定されたURLから課題データを取得し、allAssignmentsに格納
      const url = assignment.url
      const response = await fetch('http://localhost:5000/api/assignments', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url })
      })
      if (!response.ok) {
        throw new Error('課題データの取得に失敗しました')
      }

      const data = await response.json()
      allAssignments.value.push(data)
      allAssignments.value.sort((a, b) => a.id - b.id)

      changeAssignment(0)
    } catch (e) {
      console.error(e)
    }
  })
}

// storeに現在の課題を保持すると同時に、選択された課題のIDをローカルに保持する
function changeAssignment(index: number) {
  // 課題が存在するか確認
  if (allAssignments.value.length > 0 && allAssignments.value[index]) {
    store.selectedAssignment = allAssignments.value[index]
    selectedAssignmentId.value = allAssignments.value[index].id
  } else {
    console.error(`Assignment at index ${index} not found.`)
  }
}

defineExpose({
  getAllAssignments,
  changeAssignment
})
</script>

<style scoped>
.v-tabs {
  justify-content: center;
}
</style>
