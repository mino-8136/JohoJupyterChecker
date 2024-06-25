<template>
  <v-form>
    <v-file-input
      color="primary"
      label=".ipynbファイルを選択する"
      v-model="file"
      @change="submitForm"
    ></v-file-input>
  </v-form>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const file = ref<File | null>(null)
const assignments = ref<Array<{ name: string, status: string }>>([
  { name: '課題1', status: '未提出' }, // サンプルデータ
  { name: '課題2', status: '未提出' }
])

const submitForm = () => {
  if (!file.value) {
    alert('ファイルを選択してください')
    return
  }

  const formData = new FormData()
  formData.append('file', file.value)

  fetch('http://localhost:5000/api/submit', {
    method: 'POST',
    body: formData
  })
    .then(response => response.json())
    .then(data => {
      console.log(data)
      updateAssignmentStatus(data.assignments)
    })
    .catch(error => {
      console.error('Error:', error)
    })
}

const updateAssignmentStatus = (results: Array<{ name: string, status: string }>) => {
  results.forEach(result => {
    const assignment = assignments.value.find(a => a.name === result.name)
    if (assignment) {
      assignment.status = result.status === 'clear!' ? '正解' : '不正解'
    }
  })
}
</script>

<style scoped>
.v-file-input {
  margin: 2em 0;
}
</style>
