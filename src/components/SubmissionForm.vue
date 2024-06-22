<template>
  <v-form>
    <v-file-input
      color="primary"
      label="IPYNBファイルを選択する"
      v-model="file"
      @change="submitForm"
    ></v-file-input>
  </v-form>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const file = ref<File | null>(null)
const studentId = ref<string>('')
const assignments = ref<Array<{ name: string, status: string }>>([]) // 既存の assignments を参照

const submitForm = () => {
  if (!file.value) {
    alert('ファイルを選択してください')
    return
  }

  const formData = new FormData()
  formData.append('file', file.value)
  formData.append('studentId', studentId.value)

  fetch('http://localhost:5000/api/submit', {
    method: 'POST',
    body: formData
  })
    .then(response => response.json())
    .then((data: any) => {
      console.log(data)
      updateAssignmentStatus(data)
    })
    .catch((error: any) => {
      console.error('Error:', error)
    })
}

const updateAssignmentStatus = (results: Array<{ name: string, status: boolean }>) => {
  results.forEach(result => {
    const assignment = assignments.value.find(a => a.name === result.name)
    if (assignment) {
      assignment.status = result.status ? '正解' : '不正解'
    }
  })
}
</script>

<style scoped>
.v-file-input {
  margin: 2em 0;
}
</style>
