<template>
  <v-tabs v-model:active="selectedAssignmentIndex" grow>
    <v-tab
      v-for="(assignment, index) in assignments"
      :key="assignment.id"
      @click="changeAssignment(index)"
    >
      {{ assignment.name }}
    </v-tab>
  </v-tabs>
</template>

<script setup lang="ts">
import { ref, defineEmits, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

// TODO:Assignment型は共通化していい気がする
interface Assignment {
  id: number
  name: string
  link: string
}

const emit = defineEmits(['callCatchAssignmentId']) // 親に課題情報を返すためのemit関数
const selectedAssignmentIndex = ref(0) // 課題の選択状態を管理
const assignments = ref<Array<Assignment>>([])
const router = useRouter() // Vue Routerのインスタンスを取得
const route = useRoute() // 現在のルート情報を取得

// データの取得とリンクの生成
function generateAssignmentTabs() {
  const numAssignments = 4
  const AssignmentData = []
  for (let i = 1; i <= numAssignments; i++) {
    AssignmentData.push({
      id: i,
      name: `${i}週目`,
      link: `public/static/problems/week${i}.json`
    })
  }
  assignments.value = AssignmentData
}

function changeAssignment(index: number) {
  selectedAssignmentIndex.value = index

  // 親に週情報を返す -> storeに保持する
  emit('callCatchAssignmentId', selectedAssignmentIndex.value)

  // ルーターを使ってページ遷移を行う
  router.push({ name: 'assignment', params: { id: assignments.value[index].id } })
}

onMounted(() => {
  generateAssignmentTabs()

  // URLパラメータから初期値を設定
  const initialId = parseInt(route.params.id as string, 10) - 1
  if (initialId >= 0 && initialId < assignments.value.length) {
    selectedAssignmentIndex.value = initialId
  }
  console.log(route.params, route.params.id, initialId)
})
</script>

<style scoped>
.v-tabs {
  justify-content: center;
}
</style>
