import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { Assignment, Status } from '../assets/Commons'

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

    // 各課題の得点を計算する関数
    const getProblemScore = (problemIndex: number) => {
      return computed(() => {
        const problem = selectedAssignment.value.problems[problemIndex]
        const correctResultsCount = problem.testCases.filter(
          (testCase) => testCase.status == Status.Correct
        ).length
        return (correctResultsCount / problem.testCases.length) * problem.points
      })
    }

    // 全体の最大得点を計算する関数
    const getTotalScore = computed(() => {
      return selectedAssignment.value.problems.reduce((total, problem) => total + problem.points, 0)
    })

    // 現在の得点を計算する関数
    const getCurrentScore = computed(() => {
      return selectedAssignment.value.problems.reduce((totalScore, problem) => {
        if (problem.testCases?.length > 0) {
          const correctResultsCount = problem.testCases.filter(
            (cases) => cases.status == Status.Correct
          ).length
          const problemScore = (correctResultsCount / problem.testCases.length) * problem.points
          return totalScore + problemScore
        }
        return totalScore
      }, 0)
    })
    return {
      selectedAssignment,
      getProblemScore,
      getTotalScore,
      getCurrentScore
    }
  },

  {
    persist: true
  }
)
