<template>
  <v-table class="elevation-1">
    <thead>
      <tr class="header-row">
        <th class="text-left">課題</th>
        <th class="text-left">課題点</th>
        <th class="text-left">達成状況</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="assignment in assignments" :key="assignment.name">
        <td>{{ assignment.name }}</td>
        <td>{{ assignment.points }}</td>
        <td>
          <v-chip v-if="assignment.status" color="success" dark>
            {{ assignment.status }}
          </v-chip>
          <v-chip v-else color="error" dark> 未完了 </v-chip>
        </td>
      </tr>
    </tbody>
  </v-table>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'

const prop = defineProps<{
  week: number
}>()

interface Assignment {
  name: string
  points: number
  status: string | null
}

const assignments = ref<Assignment[]>([])

// TODO : problemDescriptionと同じ内容
function getWeekFileName(week: number): string {
  return `static/problems/week${week + 1}.json`
}

function getAssignments(week: number) {
  fetch(getWeekFileName(week))
    .then((response) => {
      if (!response.ok) {
        throw new Error('課題データが読み込めませんでした！')
      }
      return response.json()
    })

    .then((data) => {
      assignments.value = data.assignments.map((assignment: any) => {
        return {
          name: assignment.name,
          points: assignment.points,
          status: null // 初期状態では達成状況は未設定
        }
      })
    })
    .catch((error) => {
      assignments.value = []
    })
}

// 配列データが返ってくると想定
function updateAssignmentsStatus(result) {
  const data = result

  //assingmentsのstatusを更新する
  console.log(data)
  assignments.value.forEach((assignment, index) => {
    if (data[index] != null){
      assignment.status = data[index].is_correct
    } 
  })
}

onMounted(() => {
  getAssignments(prop.week)
})

watch(
  () => prop.week,
  (week) => {
    getAssignments(week)
  }
)

defineExpose({
  updateAssignmentsStatus
})
</script>

<style scoped>
.v-table {
  margin: 3em 0em;
}

.header-row {
  background-color: #1867c0; /* ヘッダーの背景色を設定 */
  color: white; /* ヘッダーの文字色を設定 */
}
</style>
