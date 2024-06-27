<script setup lang="ts">
import WeekSelector from './components/WeekSelector.vue'
import ProblemDescription from './components/ProblemDescription.vue'
import AssignmentTable from './components/AssignmentTable.vue'
import SubmissionForm from './components/SubmissionForm.vue'
import StudentScore from './components/StudentScore.vue'

import { ref } from 'vue'

const selected_week = ref<number>(0)
const childAssignmentTable = ref<typeof AssignmentTable | null>(null)

// 週の情報を設定する(emit用)
function catchWeek(week: number) {
  selected_week.value = week
  console.log(week)
}

// 課題の状態を更新する(emit用)
function catchAssignmentsStatus(data: Array<{ name: string, status: string }>) {
  childAssignmentTable.value?.updateAssignmentsStatus(data)
}


</script>

<template>
  <v-app>
    <v-container>
      <v-app-bar app color="primary">
        <v-toolbar-title>課題自動ジャッジシステム v1.0</v-toolbar-title>
        <v-btn icon>
          <v-icon>mdi-menu</v-icon>
        </v-btn>
      </v-app-bar>
      <v-main>
        <WeekSelector @callCatchWeek="catchWeek" />
        <ProblemDescription :week="selected_week" />
        <SubmissionForm @callCatchAssignmentsStatus="catchAssignmentsStatus"/>
        <AssignmentTable ref="childAssignmentTable" :week="selected_week" />
        <StudentScore />
      </v-main>
    </v-container>
  </v-app>
</template>
