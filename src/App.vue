<script setup lang="ts">
import WeekSelector from './components/WeekSelector.vue'
import AssignmentTable from './components/AssignmentTable.vue'
import SubmissionForm from './components/SubmissionForm.vue'
import StudentScore from './components/StudentScore.vue'
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
          <WeekSelector />
          <h3 class="my-4">【1週目】Pythonの基本</h3>
          <p>何事も最初が肝心。まずはソフトの操作方法から慣れていこう。</p>
          <SubmissionForm />
          <AssignmentTable />
          <StudentScore />
      </v-main>
    </v-container>
  </v-app>
</template>
