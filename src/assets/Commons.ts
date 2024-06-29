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
      (p: any) => new Problem(p.name, p.points, p.input_example, p.output_example, p.description)
    )
    return new Assignment(json.id, json.title, json.description, problems)
  }
}

class Problem {
  name: string
  points: number
  input_example: string
  output_example: string
  description: string

  constructor(
    name: string,
    points: number,
    input_example: string,
    output_example: string,
    description: string
  ) {
    this.name = name
    this.points = points
    this.input_example = input_example
    this.output_example = output_example
    this.description = description
  }
}
