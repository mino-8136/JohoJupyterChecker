<script setup lang="ts">
import AssignmentDescription from '../components/AssignmentDescription.vue'
import AssignmentTable from '../components/AssignmentTable.vue'
import SubmissionForm from '../components/SubmissionForm.vue'
import StudentScore from '../components/StudentScore.vue'

// import { ref } from "vue";

// const childAssignmentTable = ref<typeof AssignmentTable | null>(null)

// // 課題の状態を更新する(emit用) -> storeにする
// function catchAssignmentsStatus(data: string) {
//   childAssignmentTable.value?.updateAssignmentsStatus(data)
// }
</script>

<template>
    <v-container>
        <AssignmentDescription /> 
        <!-- <SubmissionForm @callCatchAssignmentsStatus="catchAssignmentsStatus" />
        <AssignmentTable ref="childAssignmentTable" /> -->
        <StudentScore />
    </v-container>
</template>
