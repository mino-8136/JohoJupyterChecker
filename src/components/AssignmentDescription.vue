<template>
  <h3 class="my-4">{{ store.selectedAssignment.title }}</h3>
  <p>{{ store.selectedAssignment.description }}</p>
</template>

<script setup lang="ts">
import { useAssignmentStore } from '../stores/assignmentStore'
const store = useAssignmentStore() // storeのインスタンスを取得
</script>
