<script setup lang="ts">
import AssignmentDescription from '../components/AssignmentDescription.vue'
import ProblemsTable from '../components/ProblemsTable.vue'
import SubmissionForm from '../components/SubmissionForm.vue'
import StudentScore from '../components/StudentScore.vue'

</script>

<template>
    <v-container>
        <AssignmentDescription /> 
        <SubmissionForm />
        <ProblemsTable />
        <!-- <StudentScore /> -->
    </v-container>
</template>
