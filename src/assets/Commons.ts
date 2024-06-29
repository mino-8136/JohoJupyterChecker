export class Assignment {
  id: number
  title: string
  description: string
  assignments: Problem[]

  constructor() {
    this.id = 0
    this.title = ''
    this.description = ''
    this.assignments = []
  }
}

export class Problem {
  name: string
  points: number
  isCompleted: string

  constructor() {
    this.name = ''
    this.points = 0
    this.isCompleted = ''
  }
}
