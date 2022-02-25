# noo

Easily create new projects.

## Installation

```sh
pip install pynoo
```

or install from github

```sh
pip install git+https://github.com/py-noo/noo
```

## Contributing

See [contributing](./.github/CONTRIBUTING.md).

## Usage

```sh
noo clone <name> <ref>
```

## Noofile Specification

```yml
name: str
remote: str
read: [Read]
steps: [Step]
```

| Field  | Type       | Description                            |
|--------|------------|----------------------------------------|
| name   | str        | The name of the noofile definition     |
| remote | str        | The remote location of the template    |
| read   | list[Read] | The list of variables to read on setup |
| steps  | list[Step] | The list of steps to run               |

### Read

```yml
name: str
prompt: str
default: ?str
```

| Field   | Type | Description                                     |
|---------|------|-------------------------------------------------|
| name    | str  | The name of the variable to read                |
| prompt  | str  | The prompt to display when reading the variable |
| default | ?str | An optional default value                       |

### Step

A step defines a single step in the process of setting up a project.

```yml
name: str
actions: [Action]
conditions: ?[Condition]
```

| Field      | Type             | Description                                                 |
|------------|------------------|-------------------------------------------------------------|
| name       | str              | The name of the setup step                                  |
| actions    | list[Action]     | The list of actions in the step                             |
| conditions | ?list[Condition] | An optional list of conditions required for the step to run |

### Condition

A condition is a function that must be true for a step to run.

```yml
op: eq | ne | gt | lt | ge | le
var: str
value: str
```

| Field | Type       | Description                            |
|-------|------------|----------------------------------------|
| op    | Literal[eq | ne                                     |
| var   | str        | The variable to compare, i.e. noo:year |
| value | str        | The value to compare to                |

### Action

An action defined a single action within a step. This is the base of all steps, for example replacing a string with a different given string.

#### Replace action

Replace actions are used to replace a specific string in a file. The `src` field specifies the string that should be replaced in the file, and the `dest` field specifices the string to replace it with. The `dest` field is formatted with defined variables.

A list of files can be provided, and each file will have the same transform applied to them.

```yml
- action: replace
  files: [str]
  src: str
  dest: str
```

#### Delete action

Delete actions are used to delete files.

```yml
- action: delete
  files: [str]
```

#### Create action

Create actions are used to create files. The `file` field specifies the file to be created, and the `content` field specifics the content to be placed into the file. The `content` field is formatted with defined variables.

```yml
- action: create
  file: str
  content: ?str
```

#### Rename action

Rename actions are used to rename files. The `file` field specifies the file to be renamed, and the `dest` field specifies the new name of the file. The `dest` field is formatted with defined variables.

```yml
- action: rename
  file: str
  dest: str
```

### Variables

Variables are defined in the `read` section of the noofile. All variables set in the `read` section will be available in the `steps` section.

Variables are used in the format `$${scope}:{name}`, for example `$$noo:year` or `$$var:author`. Variables with the `noo` scope are built into noo and will always be available. Variables with the `var` scope are defined in the `read` section.

The variables defined by noo are:

- `noo:year` - The current year
- `noo:month` - The current month
- `noo:day` - The current day
- `noo:hour` - The current hour
- `noo:minute` - The current minute
- `noo:second` - The current second
- `noo:name` - The name of the project
