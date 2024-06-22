<template>
  <v-card class="my-4" >
    <v-card-title > あなたの得点 </v-card-title>
    <v-card-text>
      <v-row align="center" justify="center">
        <v-col cols="12" md="4">
          <v-progress-circular :value="score" :size="120" :width="15" color="primary">
            {{ score }}
          </v-progress-circular>
        </v-col>
        <v-col cols="12" md="8">
          <p>ほぼできています！お疲れさまでした。</p>
          <v-text-field label="学年組番号の4桁" v-model="studentId"></v-text-field>
          <v-btn color="primary" @click="copyResult">提出用に結果をコピー</v-btn>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const score = ref(75)
const studentId = ref('')

const copyResult = () => {
  const result = `Score: ${score.value}, ID: ${studentId.value}`
  navigator.clipboard.writeText(result).then(() => {
    alert('結果がクリップボードにコピーされました')
  })
}
</script>
