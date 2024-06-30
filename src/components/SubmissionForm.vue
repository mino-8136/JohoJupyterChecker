<template>
  <v-form v-if="store.selectedAssignment.problems.length">
    <v-btn color="primary" text=".ipynbファイルを採点する" :loading="loading" @click="(() => {
      select_file()
    })" class="rounded-pill ma-8 d-flex mx-auto">
      <template v-slot:loader >
        <v-progress-circular indeterminate width="2"></v-progress-circular>
      </template>
    </v-btn>
    <v-file-input ref="file_input" v-model="file" @change="submitForm" style="display:none;"></v-file-input>
  </v-form>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAssignmentStore } from '../stores/assignmentStore'
import { Assignment } from '../assets/Commons'

const store = useAssignmentStore()
const file = ref<File | null>(null)
const assignments = ref<Assignment>()
const loading = ref(false)
const file_input = ref<HTMLInputElement | null>(null)
const select_file = () => {
  if (file_input.value) {
    file_input.value.click()
  }
}

// ファイルを選択してPythonに送信し、その結果をStoreに保存する
async function submitForm() {
  if (!file.value) {
    alert('ファイルを選択してください')
    return
  }

  // Pythonにファイルと課題データ(Assignments全体)を送信
  const formData = new FormData()
  assignments.value = store.selectedAssignment
  formData.append('file', file.value)
  formData.append('assignments', JSON.stringify(assignments.value))
  loading.value = true

  try {
    const response = await fetch('http://localhost:5000/api/submit', {
      method: 'POST',
      body: formData
    })
    const data = await response.json()
    console.log(data)

    // Storeに結果を保存
    store.selectedAssignment.problems.forEach((problem, index) => {
      problem.results = data[index].results
    })
  } catch (error) {
    console.error('Error:', error)
  }

  // 読み込みが終わったらファイルをクリアする
  file.value = null
  loading.value = false;
}
</script>

<style scoped>
.v-file-input {
  margin: 2em 0;
}
</style>
