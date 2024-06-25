<script setup lang="ts">
import WeekSelector from './components/WeekSelector.vue'
import ProblemDescription from './components/ProblemDescription.vue'
import AssignmentTable from './components/AssignmentTable.vue'
import SubmissionForm from './components/SubmissionForm.vue'
import StudentScore from './components/StudentScore.vue'

import { ref } from 'vue'

// 週の情報を設定する
const selected_week = ref<number>(0)
function catchWeek(week: number) {
  selected_week.value = week
  console.log(week)
}

</script>

<template>
  <v-app>
    <v-container>
      <v-app-bar app color="primary" >
        <v-toolbar-title >課題自動ジャッジシステム v1.0</v-toolbar-title>
        <v-btn icon>
          <v-icon>mdi-menu</v-icon>
        </v-btn>
      </v-app-bar>
      <v-main>
          <WeekSelector @callCatchWeek="catchWeek" />
          <ProblemDescription :week=selected_week />
          <SubmissionForm />
          <AssignmentTable />
          <StudentScore />
      </v-main>
    </v-container>
  </v-app>
</template>
