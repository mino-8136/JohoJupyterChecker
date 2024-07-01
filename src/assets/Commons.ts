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
      (p: any) => new Problem(p.name, p.points, p.examples)
    )
    return new Assignment(json.id, json.title, json.description, problems)
  }
}

class Problem {
  name: string
  points: number
  examples: Example[]
  results: Results[]

  constructor(name: string, points: number, examples: Example[]) {
    this.name = name
    this.points = points
    this.examples = examples
    this.results = [] // 最初は空の配列
  }
}

class Example {
  input: string
  output: string

  constructor(input: string, output: string) {
    this.input = input
    this.output = output
  }
}

export class Results {
  input: string
  expected_output: string
  received_output: string
  status: Status

  constructor(input: string, expected_output: string, received_output: string, status: Status) {
    this.input = input
    this.expected_output = expected_output
    this.received_output = received_output
    this.status = status
  }
}

enum Status {
  Correct = '正解',
  Incorrect = '不正解',
  Error = 'エラー',
  Unanswered = '未回答'
}