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
import { ref, onMounted } from 'vue'
import { useAssignmentStore } from '../stores/assignmentStore'
import { Assignment } from '../assets/Commons'

const store = useAssignmentStore() // storeのインスタンスを取得
const allAssignments = ref<Array<Assignment>>([]) // 全課題の情報をローカル管理

// デフォルトのAssignmentインスタンスを生成する関数
function createDefaultAssignment(id: number): Assignment {
  return new Assignment(
    id,
    `課題${id}`,
    `課題${id}はまだ未定です`,
    []
  )
}

// JSONファイルから課題の情報を取得する
async function getAssignmentDataFromJSON(assignmentId: number): Promise<Assignment> {
  const jsonPath = `static/assignments/week${assignmentId}.json`
  try {
    const response = await fetch(jsonPath)
    if (!response.ok) {
      throw new Error('課題パスにアクセスできません')
    }
    const json = await response.json()
    return Assignment.fromJSON(json)
  } catch (error) {
    // console.error(`Failed to load JSON for assignment ${assignmentId}:`, error)
    return createDefaultAssignment(assignmentId)
  }
}

// 全Assignmentデータの取得(TODO: 本来はAPIから取得する。Pythonからファイル名一覧を取得し、JSONを読み込み、IDでソートする)
async function generateAssignmentTabs() {
  const numAssignments = 4
  const assignmentData: Assignment[] = []
  for (let i = 1; i <= numAssignments; i++) {
    const assignment = await getAssignmentDataFromJSON(i)
    assignmentData.push(assignment)
  }
  allAssignments.value = assignmentData
}

// storeに現在の課題を保持する
function changeAssignment(index: number) {
  store.selectedAssignment = allAssignments.value[index]
}

onMounted(async () => {
  await generateAssignmentTabs()
})
</script>

<style scoped>
.v-tabs {
  justify-content: center;
}
</style>
