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
const emit = defineEmits(['callCatchAssignmentsStatus'])

// ファイルを選択してPythonに送信し、その結果をApp.vue経由でAssignmentTableに反映する
function submitForm() {
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
    .then((response) => response.json())
    .then((data) => {
      console.log(data)
      emit('callCatchAssignmentsStatus', data)
    })
    .catch((error) => {
      console.error('Error:', error)
    })
}
</script>

<style scoped>
.v-file-input {
  margin: 2em 0;
}
</style>
