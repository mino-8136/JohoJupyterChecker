<template>
  <v-table class="elevation-1">
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
            >
              {{ result.status }}
            </v-chip>
          </div>
        </td>
      </tr>
    </tbody>
  </v-table>
</template>

<script setup lang="ts">
import { useAssignmentStore } from '../stores/assignmentStore'
const store = useAssignmentStore()
</script>

<style scoped>
.v-table {
  margin: 3em 0em;
}

.header-row {
  background-color: #1867c0; /* ヘッダーの背景色を設定 */
  color: white; /* ヘッダーの文字色を設定 */
}

.chip-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px; /* チップ間のスペースを設定 */
}
</style>
