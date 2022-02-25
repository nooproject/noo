# noo

Easily create new projects.

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
```

| Field   | Type         | Description                     |
|---------|--------------|---------------------------------|
| name    | str          | The name of the setup step      |
| actions | list[Action] | The list of actions in the step |

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
