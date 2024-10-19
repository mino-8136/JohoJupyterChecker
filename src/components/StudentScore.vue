<template>
  <v-card v-if="store.selectedAssignment.problems.length" class="elevation-8">
    <v-card-title class="bg-primary pa-4"> あなたの得点</v-card-title>
    <v-divider></v-divider>
    <v-card-text class="mx-4">
      <v-row align="center" justify="center" class="pb-4">
        <v-col cols="4">
          <v-progress-circular :model-value="(currentScore / totalScore) * 100" :size="120" :width="15" color="primary">
            <div class="score">
              <span class="number">{{ Math.floor((currentScore / totalScore) * 100) }}</span>
              <span class="percent">%</span>
            </div>
          </v-progress-circular>
        </v-col>
        <v-col cols="8">
          <p>{{ comment() }}</p>
        </v-col>
      </v-row>
      <v-divider></v-divider>
    </v-card-text>
    <v-card-text align="center" class="px-8">
      <v-text-field label="学年組番号の4桁" v-model="studentId" density="comfortable" variant="outlined" width="85%" :rules="[rules.number]">
        <template v-slot:append>
          <v-btn color="primary" @click="copyResult" class="rounded-pill" :disabled="!isStudentIdValid">提出用に結果をコピー</v-btn>
        </template>
      </v-text-field>
    </v-card-text>
  </v-card>

  <v-dialog v-model="dialog" width="auto" min-width="400px">
    <v-card>
      <v-card-title class="bg-correct py-2">
        <v-icon icon="mdi-check-bold" class="me-2"></v-icon>
        成功！
      </v-card-title>
      <v-card-text>
        <p>データがクリップボードにコピーされました。</p>
        <p>このままPC室のFormリンクか、<br>Teamsの課題に貼り付けて提出してください。</p>
      </v-card-text>
      <v-divider></v-divider>
      <template v-slot:actions>
        <v-btn class="ms-auto" @click="dialog = false">Ok</v-btn>
      </template>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useAssignmentStore } from '../stores/assignmentStore'
import CryptoJS from 'crypto-js'

const store = useAssignmentStore()
const totalScore = computed(() => store.getTotalScore)
const currentScore = computed(() => store.getCurrentScore)
const dialog = ref(false)

const studentId = ref('')
const rules = {
  number: (v: string) => v === '' || /^\d{4}$/.test(v) || '4桁の半角数字で入力',
}
const isStudentIdValid = computed(() => {
  return /^\d{4}$/.test(studentId.value)
})

function comment() {
  const grade = currentScore.value / totalScore.value
  if (grade >= 0.99) {
    return '素晴らしい！満点です！'
  } else if (grade >= 0.9) {
    return 'よくできました！'
  } else if (grade >= 0.7) {
    return 'ほぼできています！お疲れさまでした。'
  } else if (grade >= 0.5) {
    return 'その調子です！'
  } else {
    return '頑張りましょう！'
  }
}

function copyResult() {
  if (!isStudentIdValid.value) {
    alert('学年組番号を正しく入力してください')
    return
  }

  const assignmentData = store.selectedAssignment;
  const assignmentTitle = assignmentData.title;
  const score = currentScore.value;

  // 暫定的に、文字列とassignmentTitleと入力IDとスコアをアンダーバーで繋いだものをキーとして使用
  const encryptionKey = `kadaiJudge_${assignmentTitle}_${studentId.value}_${score}`;
  
  // 入力IDとスコアをキーとしてstore.selectedAssignmentを暗号化(TODO : バックエンドへ移す)
  const encryptedData = CryptoJS.AES.encrypt(JSON.stringify(assignmentData), encryptionKey).toString();
  
  const result = {
    assignmentTitle: assignmentTitle,
    studentId: studentId.value,
    score: score,
    encryptedData: encryptedData
  };
  
  navigator.clipboard.writeText(JSON.stringify(result)).then(() => {
    dialog.value = true;
  }).catch(err => {
    console.error('コピーに失敗しました:', err);
  });
  
  // 検出できる不正 : 別の課題で実行したスコアを提出した・スコアを書き換えた・他人の学年組番号を入力して提出した
  // テスト用キー例 : kadaiJudge_①Pythonの基本_1234_240
}
</script>

<style scoped>
.score {
  display: inline-flex;
  align-items: baseline;
  font-weight: bold;
  margin-left: 3px;
}

.number {
  font-size: 1.75em;
}

.percent {
  font-size: 1em;
}
</style>
