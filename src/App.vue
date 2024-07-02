<script setup lang="ts">
import AssignmentSelector from './components/AssignmentSelector.vue'
import AssignmentView from './views/AssignmentView.vue'
</script>

<template>
  <v-app>
    <v-app-bar app color="primary" class="py-1">
      <template v-slot:prepend>
        <v-btn icon>
          <v-icon>mdi-menu</v-icon>
        </v-btn>
      </template>
      <v-app-bar-title>
        課題自動ジャッジシステム
      </v-app-bar-title>
    </v-app-bar>
    <v-main>
      <AssignmentSelector />
      <AssignmentView />
    </v-main>
  </v-app>
</template>
