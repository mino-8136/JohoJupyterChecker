<template>
  <v-app>
    <v-app-bar app color="primary" class="py-1">
      <v-app-bar-title> 課題自動ジャッジシステム </v-app-bar-title>
      <template v-slot:append>
        <v-select
        class="mt-6 mr-3"
          label="コース選択"
          :items="allCourses"
          v-model="store.selectedCourse"
          variant="outlined"
        >
        </v-select>
      </template>
    </v-app-bar>
    <v-main>
      <AssignmentSelector />
      <AssignmentView />
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import AssignmentSelector from './components/AssignmentSelector.vue'
import AssignmentView from './views/AssignmentView.vue'
import { useAssignmentStore } from '@/stores/assignmentStore'

const store = useAssignmentStore()
const allCourses = ref<string[]>([])

// Pythonからcourse内のディレクトリ名を取得する
async function getCourseDirectories() {
  try {
    const response = await fetch('http://localhost:5000/api/courses', {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' }
    })
    if (!response.ok) {
      throw new Error('コースデータの取得に失敗しました')
    }

    const data = await response.json()
    data.forEach((course: string) => {
      allCourses.value.push(course)
    })
  } catch (e) {
    console.error(e)
  }
}

onMounted(async () => {
  // コース一覧の取得と初期コースの設定
  await getCourseDirectories()
  const defaultCourse = 'python_basic_101'
  const findDefaultCourse = allCourses.value.find((course) => course === defaultCourse)
  if (findDefaultCourse) {
    store.selectedCourse = defaultCourse
  }
})
</script>
