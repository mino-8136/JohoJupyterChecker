import { ref, computed } from 'vue'
import { defineStore } from 'pinia'


const 


export const useAssignmentStore = defineStore('assignment', () => {
  const assignments = ref([])

  function updateAssignmentsStatus(data: Array<{ name: string, status: string }>) {
    assignments.value = data
  }
})