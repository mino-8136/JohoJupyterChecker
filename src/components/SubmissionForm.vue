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

// TODO : Assignmentはstoreで保持したほうが管理がしやすい
interface Assignment {
  input_example: string
  output_example: string
}

const file = ref<File | null>(null)
const assignments = ref<Assignment[]>([])
const emit = defineEmits(['callCatchAssignmentsStatus'])
const props = defineProps<{
  week: number
}>()

// TODO : 他のファイルと同じ実装になっているので、共通化する
function getWeekFileName(week: number): string {
  return `static/problems/week${week + 1}.json`
}

// 課題の情報を取得する
async function getAssignments(week: number) {
  const response = await fetch(getWeekFileName(week))
  const data = await response.json()
  assignments.value = data.assignments.map((assignment: Assignment) => ({
    input_example: assignment.input_example,
    output_example: assignment.output_example
  }))

  // console.log(assignments.value)
}

// ファイルを選択してPythonに送信し、その結果をApp.vue経由でAssignmentTableに反映する
async function submitForm() {
  if (!file.value) {
    alert('ファイルを選択してください')
    return
  }

  getAssignments(props.week)

  const formData = new FormData()
  formData.append('file', file.value)
  formData.append('assignments', JSON.stringify(assignments.value))

  try {
    const response = await fetch('http://localhost:5000/api/submit', {
      method: 'POST',
      body: formData
    })
    const data = await response.json()
    emit('callCatchAssignmentsStatus', data)
    // console.log(data)
  } catch (error) {
    console.error('Error:', error)
  }
}
</script>

<style scoped>
.v-file-input {
  margin: 2em 0;
}
</style>
