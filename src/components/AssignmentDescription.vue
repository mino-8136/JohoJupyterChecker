<template>
  <v-container>
    <h2 class="my-4 text-center" >{{ store.selectedAssignment.title }}</h2>
    <p class="text-center"> {{ store.selectedAssignment.description }}</p>
  </v-container>
</template>

<script setup lang="ts">
import { useAssignmentStore } from '../stores/assignmentStore'
const store = useAssignmentStore() // storeのインスタンスを取得
</script>
