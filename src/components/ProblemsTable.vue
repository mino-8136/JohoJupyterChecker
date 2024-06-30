<template>
  <v-table v-if="store.selectedAssignment.problems.length" class="elevation-2">
    <thead>
      <tr class="header-row">
        <th class="text-left" width="25%">課題</th>
        <th class="text-left" width="25%">課題点</th>
        <th class="text-left">達成状況</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="problem in store.selectedAssignment.problems" :key="problem.name">
        <td>{{ problem.name }}</td>
        <td>{{ problem.points }}</td>
        <td>
          <div class="chip-container">
            <v-chip
              v-for="result in problem.results"
              :key="result.input"
              :color="result.status ? 'success' : 'error'"
              @click="openDialog(result)"
            >
              {{ result.status }}
            </v-chip>
          </div>
        </td>
      </tr>
    </tbody>
  </v-table>

  <v-dialog v-model="dialog" width="auto" min-width="400px">
    <v-card>
      <v-card-title :class="selectedResult?.status ? 'success-title' : 'error-title'" class="py-4">
        <v-icon
          :icon="selectedResult?.status ? 'mdi-check-bold' : 'mdi-exclamation-thick'"
          class="me-2"
        ></v-icon>
        {{ selectedResult?.status ? '正解です' : '結果の見直しが必要です' }}
      </v-card-title>
      <v-card-text>
        <div v-if="selectedResult">
          <p><strong>入力例:</strong></p>
          <p class="mb-2">{{ selectedResult.input }}</p>
          <p><strong>出力例:</strong></p>
          <p class="mb-2">{{ selectedResult.expected_output }}</p>
          <p><strong>あなたの実行結果:</strong></p>
          <p class="mb-2">{{ selectedResult.received_output }}</p>
        </div>
      </v-card-text>
      <v-divider></v-divider>
      <template v-slot:actions>
        <v-btn class="ms-auto" @click="dialog = false">Ok</v-btn>
      </template>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { useAssignmentStore } from '../stores/assignmentStore'
import { Results } from '@/assets/Commons'
import { ref } from 'vue'

const store = useAssignmentStore()
const dialog = ref(false)
const selectedResult = ref<Results | null>(null)

function openDialog(result: Results) {
  selectedResult.value = result
  dialog.value = true
}
</script>

<style scoped>
.v-table {
  margin: 3em 0em;
}

.header-row {
  background-color: #ededed; /* ヘッダーの背景色を設定 */
}

.chip-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px; /* チップ間のスペースを設定 */
}

.success-title {
  background-color: #4caf50; /* 背景色を緑に設定 */
  color: white;
}

.error-title {
  background-color: #f44336; /* 赤色の背景 */
  color: white;
}
</style>
