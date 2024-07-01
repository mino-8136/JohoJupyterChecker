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
        <td> 0 / {{ problem.points }}</td>
        <td>
          <div class="chip-container">
            <v-chip
              v-for="testCase in problem.testCases"
              :key="testCase.input"
              :color="getColor(testCase.status)"
              @click="openDialog(testCase)"
            >
              {{ testCase.status }}
            </v-chip>
          </div>
        </td>
      </tr>
    </tbody>
  </v-table>

  <v-dialog v-model="dialog" width="auto" min-width="400px">
    <v-card>
      <v-card-title :class="selectedTestCase?.status ? 'bg-success' : 'bg-warning'" class="py-4">
        <v-icon
          :icon="selectedTestCase?.status ? 'mdi-check-bold' : 'mdi-exclamation-thick'"
          class="me-2"
        ></v-icon>
        {{ selectedTestCase?.status ? '正解です' : '結果の見直しが必要です' }}
      </v-card-title>
      <v-card-text>
        <div v-if="selectedTestCase">
          <p><strong>入力例:</strong></p>
          <p class="mb-2">{{ selectedTestCase.input }}</p>
          <p><strong>出力例:</strong></p>
          <p class="mb-2">{{ selectedTestCase.output }}</p>
          <p><strong>あなたの実行結果:</strong></p>
          <p class="mb-2">{{ selectedTestCase.output_user }}</p>
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
import { TestCase, Status } from '@/assets/Commons'
import { ref } from 'vue'

const store = useAssignmentStore()
const dialog = ref(false)
const selectedTestCase = ref<TestCase | null>(null)

function getColor(status: Status){
  switch (status){
    case Status.Correct:
      return 'success'
    case Status.Incorrect:
      return 'error'
    default:
      return 'grey'
  }
}

function openDialog(result: TestCase) {
  selectedTestCase.value = result
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
</style>
