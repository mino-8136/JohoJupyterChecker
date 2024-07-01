export class Assignment {
  id: number
  title: string
  description: string
  problems: Problem[]

  constructor(id: number, title: string, description: string, problems: Problem[]) {
    this.id = id
    this.title = title
    this.description = description
    this.problems = problems
  }

  static fromJSON(json: any): Assignment {
    const problems = json.problems.map(
      (p: any) => new Problem(p.name, p.points, p.description, p.testCases)
    )
    return new Assignment(json.id, json.title, json.description, problems)
  }
}

class Problem {
  name: string
  points: number
  description: string
  testCases: TestCase[]

  constructor(name: string, points: number, description: string, testCases: TestCase[]) {
    this.name = name
    this.points = points
    this.description = description
    this.testCases = testCases
  }
}

export class TestCase {
  input: string
  output: string
  output_user: string
  status: Status

  constructor(input: string, output: string) {
    this.input = input
    this.output = output
    this.output_user = ''
    this.status = Status.Unanswered
  }
}

export enum Status {
    Correct = '正解',
    Incorrect = '不正解',
    Error = 'エラー',
    Unanswered = '未回答',
}