<script setup lang="ts">
import AssignmentSelector from './components/AssignmentSelector.vue'
import AssignmentView from './views/AssignmentView.vue'

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
        <AssignmentSelector />
        <!-- <AssignmentView /> -->
      </v-main>
    </v-container>
  </v-app>
</template>
