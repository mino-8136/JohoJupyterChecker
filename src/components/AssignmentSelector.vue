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

// 指定コース内の全課題jsonデータを読み込む(App.vueから呼び出す)
async function getAllAssignments(course: string) {
  // 既に読み込まれている課題データを初期化
  allAssignments.value = []
  store.initiateSelectedAssignment()

  // store.allCoursesJSONから指定コース名をもとに、課題jsonデータを取得
  const allCourses: AllCoursesJSON = store.allCoursesJSON
  const checkerURLs = allCourses[course].checkerURLs
  for(const checkerURL of checkerURLs){
    try{
      // 指定されたURLから課題データを取得
      const response = await fetch("http://localhost:5000/api/checker", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ checker_url: checkerURL }),
      });
      if (!response.ok) {
        throw new Error(`課題データの取得に失敗しました: ${checkerURL}`)
      }
      const data = await response.json()
      allAssignments.value.push(data)
    } catch (e) {
      console.error(e)
    }
  }

  // 課題IDでソートし、最初の課題を選択
  allAssignments.value.sort((a, b) => a.id - b.id)
  if (allAssignments.value.length > 0) {
    changeAssignment(0);
  }
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
