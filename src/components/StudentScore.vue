<template>
  <v-card class="my-4">
    <v-card-title class="header pa-4"> あなたの得点 </v-card-title>
    <v-divider></v-divider>
    <v-card-text>
      
      <v-row align="center" justify="center" cols="12">
        <v-col md="4">
          <v-progress-circular :value="score" :size="120" :width="15" color="primary">
            {{ score }}
          </v-progress-circular>
        </v-col>
        <v-col md="8">
          <p>ほぼできています！お疲れさまでした。</p>
        </v-col>
      </v-row>
      <v-divider></v-divider>
    </v-card-text>
      <v-card-text>

        <v-row align="center" justify="center" cols="12">
          <v-col>
            <v-text-field label="学年組番号の4桁" v-model="studentId"></v-text-field>
          </v-col>
          <v-col>
            <v-btn color="primary" @click="copyResult">提出用に結果をコピー</v-btn>
          </v-col>
        </v-row>
        
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
import { ref,computed } from 'vue'
import { useAssignmentStore } from '../stores/assignmentStore'

const store = useAssignmentStore()
const studentId = ref('')

function copyResult() {
  const result = `Score: ${score.value}, ID: ${studentId.value}`
  navigator.clipboard.writeText(result).then(() => {
    alert('結果がクリップボードにコピーされました')
  })
}
</script>

<style scoped>
.header {
  background-color: #1867c0; /* ヘッダーの背景色を設定 */
  color: white; /* ヘッダーの文字色を設定 */
}

</style>