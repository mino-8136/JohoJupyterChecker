<template>
    <v-table class="elevation-1">
        <thead>
            <tr  class="header-row">
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
import { ref, onMounted } from 'vue'

const assignments = ref([])
const headers = [
  { text: '課題', value: 'name' },
  { text: '課題点', value: 'points' },
  { text: '達成状況', value: 'status' }
]

onMounted(() => {
  // JSONファイルからデータを読み込む
  fetch('/problems/week1.json')
    .then((response) => {
      if (!response.ok) {
        throw new Error('Network response was not ok')
      }
      return response.json()
    })
    .then((data) => {
      assignments.value = data.assignments.map((assignment) => {
        return {
          ...assignment,
          status: null // 初期状態では達成状況は未設定
        }
      })
    })
    .catch((error) => {
      console.error('There was a problem with the fetch operation:', error)
    })
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
