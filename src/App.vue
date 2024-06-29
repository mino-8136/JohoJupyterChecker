<script setup lang="ts">
import AssignmentSelector from './components/AssignmentSelector.vue'
import AssignmentView from './views/AssignmentView.vue'

import { ref } from 'vue';

const selectedAssignment = ref<number>(1)

// 週の情報を設定する(emit用)
function catchAssignmentId(assignmentId: number) {
  selectedAssignment.value = assignmentId
  console.log(assignmentId)
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
        <AssignmentSelector  @callCatchAssignmentId="catchAssignmentId" />
        <AssignmentView />
      </v-main>
    </v-container>
  </v-app>
</template>
