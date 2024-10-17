<template>
  <v-form v-if="store.selectedAssignment.problems.length">
    <v-btn
      text=".ipynbファイルを採点する"
      color="primary"
      class="rounded-pill ma-8 d-flex mx-auto"
      style="text-transform: none"
      @click="select_file()"
      @dragover.prevent
      @drop.prevent="dropFile"
      :loading="loading"
      >
      <template v-slot:loader>
        <v-progress-circular indeterminate width="2"></v-progress-circular>
      </template>
    </v-btn>
    <v-file-input
      ref="file_input"
      v-model="file"
      @change="submitForm"
      style="display: none"
    ></v-file-input>
  </v-form>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAssignmentStore } from '../stores/assignmentStore'
import { Assignment } from './utils/Commons'

const store = useAssignmentStore()

const assignments = ref<Assignment>()
const file = ref<File | null>(null)
const file_input = ref<HTMLInputElement | null>(null)
const loading = ref(false)

function select_file() {
  if (file_input.value) {
    file_input.value.click()
  }
}

// ファイルのドロップ関連の処理
function dropFile(event: DragEvent) {
  event.preventDefault()
  const droppedFile = event.dataTransfer?.files[0]
  if (droppedFile) {
    file.value = droppedFile
  }
  submitForm()
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
      problem.testCases = data[index].results
    })
  } catch (error) {
    console.error('Error:', error)
  }

  // 読み込みが終わったらファイルをクリアする
  file.value = null
  loading.value = false
}
</script>

<style scoped>
.v-file-input {
  margin: 2em 0;
}
</style>
