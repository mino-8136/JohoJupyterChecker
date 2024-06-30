import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { Assignment } from '../assets/Commons'

// 現在読み込んでいる課題の状況を管理するストア
export const useAssignmentStore = defineStore(
  'assignment',
  () => {
    const selectedAssignment = ref<Assignment>({
      id: 1,
      title: '',
      description: '',
      problems: []
    })

    // 総得点を計算する関数
    const getTotalScore = computed(() => {
      return selectedAssignment.value.problems.reduce((total, problem) => total + problem.points, 0)
    })

    // 現在の得点を計算する関数
    const getCurrentScore = computed(() => {
      return selectedAssignment.value.problems.reduce((totalScore, problem) => {
        if (problem.results.length > 0) {
          const correctResultsCount = problem.results.filter((result) => result.status).length
          const problemScore = (correctResultsCount / problem.results.length) * problem.points
          return totalScore + problemScore
        }
        return totalScore
      }, 0)
    })
    return {
      selectedAssignment,
      getTotalScore,
      getCurrentScore
    }
  },

  {
    persist: true
  }
)
