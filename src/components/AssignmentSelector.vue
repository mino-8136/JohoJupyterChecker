<template>
  <v-tabs v-model="store.selectedAssignment.id" grow>
    <v-tab
      v-for="(assignment, index) in allAssignments"
      :key="assignment.id"
      @click="changeAssignment(index)"
    >
      {{ assignment.title }}
    </v-tab>
  </v-tabs>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { useAssignmentStore } from '../stores/assignmentStore'
import { useRouter, useRoute } from 'vue-router'
import { Assignment } from '../assets/Commons'

const router = useRouter() // Vue Routerのインスタンスを取得
const route = useRoute() // Vue Routerのルート情報を取得
const store = useAssignmentStore() // storeのインスタンスを取得
const allAssignments = ref<Array<Assignment>>([]) // 全課題の情報をローカル管理

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
      assignments:[]
    })
  }
  allAssignments.value = AssignmentData
}

// storeに現在の課題を保持したあと、ルーターを使ってページ遷移を行う
function changeAssignment(index: number) {
  store.selectedAssignment.id = allAssignments.value[index].id
  router.push({ name: 'assignment', params: { id: allAssignments.value[index].id } })
}

onMounted(() => {
  generateAssignmentTabs()
})


watch(
  () => route.params.id,
  (newId, oldId) => {
    console.log('Route param id changed from', oldId, 'to', newId)
    // ここで必要な処理を行う
    if (newId) {
      store.selectedAssignment.id = parseInt(newId as string, 10)
    }
  }
)
</script>

<style scoped>
.v-tabs {
  justify-content: center;
}
</style>
