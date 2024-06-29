<script setup lang="ts">
import ProblemDescription from '../components/ProblemDescription.vue'
import AssignmentTable from '../components/AssignmentTable.vue'
import SubmissionForm from '../components/SubmissionForm.vue'
import StudentScore from '../components/StudentScore.vue'

import { ref } from "vue";

const selected_week = ref<number>(0)
const childAssignmentTable = ref<typeof AssignmentTable | null>(null)

// 週の情報を設定する(emit用) -> storeにする
function catchWeek(week: number) {
  selected_week.value = week
  console.log(week)
}

// 課題の状態を更新する(emit用) -> storeにする
function catchAssignmentsStatus(data: string) {
  childAssignmentTable.value?.updateAssignmentsStatus(data)
}
</script>

<template>
    <v-container>
        <ProblemDescription :week="selected_week" />
        <SubmissionForm  :week="selected_week" @callCatchAssignmentsStatus="catchAssignmentsStatus" />
        <AssignmentTable ref="childAssignmentTable" :week="selected_week" />
        <StudentScore />
    </v-container>
</template>
