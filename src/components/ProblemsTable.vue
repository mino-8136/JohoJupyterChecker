<template>
  <v-table v-if="store.selectedAssignment.problems.length" class="elevation-2">
    <thead>
      <tr class="header-row">
        <th class="text-left" width="25%"><v-chip variant="text"> 課題 </v-chip></th>
        <th class="text-left" width="25%">課題点</th>
        <th class="text-left">達成状況</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(problem, index) in store.selectedAssignment.problems" :key="problem.name">
        <td>
          <v-chip
            variant="text"
            :text="problem.name"
            @click="openDescriptionDialog(problem)"
          ></v-chip>
        </td>
        <td>{{ store.getProblemScore(index) }} / {{ problem.points }}</td>
        <td>
          <div class="chip-container">
            <v-chip
              v-for="testCase in problem.testCases"
              :key="testCase.input"
              :color="getStatusInfo(testCase.status).color"
              variant="flat"
              @click="openDialog(testCase)"
            >
              <v-icon>
                {{ getStatusInfo(testCase.status).icon }}
              </v-icon>
            </v-chip>
          </div>
        </td>
      </tr>
    </tbody>
  </v-table>

  <v-dialog v-model="descriptionDialog" width="auto" min-width="400px">
    <v-card>
      <v-card-title class="pt-6 text-center">
        {{ selectedProblem?.name }}
      </v-card-title>
      <v-card-text>
        <div v-if="selectedProblem">
          <p>{{ selectedProblem.description }}</p>
        </div>
      </v-card-text>
      <v-divider></v-divider>
      <template v-slot:actions>
        <v-btn class="ms-auto" @click="descriptionDialog = false">閉じる</v-btn>
      </template>
    </v-card>
  </v-dialog>

  <v-dialog v-model="dialog" width="auto" min-width="400px">
    <v-card>
      <v-card-title :class="statusInfo.bgColor" class="py-4">
        <v-icon :icon="statusInfo.icon" class="me-2"></v-icon>
        {{ statusInfo.comment }}
      </v-card-title>
      <v-card-text>
        <div v-if="selectedTestCase">
          <p><strong>▼入力例</strong></p>
          <p class="mb-2" style="white-space: pre-wrap">{{ selectedTestCase.input }}</p>
          <p><strong>▼出力例</strong></p>
          <p class="mb-2" style="white-space: pre-wrap">{{ selectedTestCase.output }}</p>
          <p><strong>▼あなたの実行結果</strong></p>
          <p class="mb-2" style="white-space: pre-wrap">{{ selectedTestCase.output_user }}</p>
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
import { TestCase, Problem, Status } from './utils/Commons'
import { ref, computed } from 'vue'

const store = useAssignmentStore()
const dialog = ref(false)
const selectedTestCase = ref<TestCase | null>(null)
const descriptionDialog = ref(false)
const selectedProblem = ref<Problem | null>(null)

const StatusInfo = {
  [Status.Correct]: {
    icon: 'mdi-check-bold',
    color: 'correct',
    bgColor: 'bg-correct',
    comment: '正解です',
    symbol: '正解'
  },
  [Status.Incorrect]: {
    icon: 'mdi-exclamation-thick',
    color: 'orange-darken-1',
    bgColor: 'bg-orange-darken-1',
    comment: '結果の見直しが必要です',
    symbol: '不正解'
  },
  [Status.Error]: {
    icon: 'mdi-close-thick',
    color: 'error',
    bgColor: 'bg-error',
    comment: 'エラーです',
    symbol: 'エラー'
  },
  [Status.Unanswered]: {
    icon: 'mdi-help',
    color: 'grey',
    bgColor: 'bg-grey',
    comment: '未回答です',
    symbol: '未回答'
  }
}

function getStatusInfo(status: Status) {
  return StatusInfo[status] || StatusInfo[Status.Unanswered]
}

const statusInfo = computed(() => {
  return getStatusInfo(selectedTestCase.value?.status ?? Status.Unanswered)
})

function openDescriptionDialog(problem: Problem) {
  selectedProblem.value = problem
  descriptionDialog.value = true
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
  gap: 2px 8px; /* チップ間のスペースを設定 */
  padding: 8px 0px ;
}
</style>
