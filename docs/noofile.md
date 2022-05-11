# Noofiles

A noofile is a definition of a template project. It contains all the instructions required to set up a new project automatically. Example noofiles can be found [in the noo GitHub repository](https://github.com/py-noo/noo/tree/master/examples).

There are two types of noofiles, `clone` and `modify` noofiles. Clone noofiles must define a remote, while modify noofiles are just a sequence of steps. Noofiles are defined using `YAML` syntax. Since JSON is valid YAML, it is possible to use JSON as well.

## `name`

This field is the name of the Noo template. It will be used when showing messages to the user suring setup, it will not affect the template itself in any way. This field is required.

## `remote`

This field is the remote location of the template repository. This can be in two different formats currently:

- `git:` - This is the git format. It can be used like this: `git:https://github.com/vcokltfre/api-template.git`
- `file:` - This is the local file format. It can be used like this: `file:~/templates/api-template`

This field is required for cloning a noofile, but is **not** required when using `noo mod`.

## `noo_version`

This field specifies the Noo version the noofile is compatible with. The only allowed value currently is `2`. This field is required and is an integer.

## `read`

This field is a list of variables to read from the user. Each variable is defined by a [`Read`](#read-object) object. Any variables defined here can be accessed using `$$var:varname` in supported fields. This field is optional.

## `steps`

This field is the core of a noofile. It defines the steps to take to set up a new project. Each step is defined by a [`Step`](#step-object) object. This field is required.

## Variables

The following is a list of built in variables. They can be accessed by using `$$noo:varname` in supported fields.

| Name     | Description                                                  |
|----------|--------------------------------------------------------------|
| name     | The name of the noo project provided to the `clone` command. |
| year     | The current year.                                            |
| month    | The current month. (An integer starting from 1)              |
| day      | The current day. (An integer starting from 1)                |
| hour     | The current hour.                                            |
| minute   | The current minute.                                          |
| second   | The current second.                                          |
| isotime  | The current ISO8601 timestamp.                               |
| unixtime | The current Unix timestamp.                                  |

## Objects

### Read Object

| Field    | Type               | Description                                                                         |
|----------|--------------------|-------------------------------------------------------------------------------------|
| name     | str                | The name of the variable to read.                                                   |
| prompt   | str                | The prompt to display when reading the variable.                                    |
| default  | ?str               | An optional default value.                                                          |
| required | bool; default=true | Whether this varable must be a non-empty string.                                    |
| match    | ?str               | An optional regex the input must match. Wrap this in `^..$` to ensure a full match. |

### Step Object

| Field      | Type                                  | Description                                                  |
|------------|---------------------------------------|--------------------------------------------------------------|
| name       | str                                   | The name of the setup step.                                  |
| actions    | list[[Action](#action-objects)]       | The list of actions in the step.                             |
| conditions | ?list[[Condition](#condition-object)] | An optional list of conditions required for the step to run. |

### Action Objects

The `formatted` column of action descriptions below shows whether the field is formatted with the defined variables.

#### Replace action

Replace actions are used to replace a specific string in a file.

| Field  | Type             | Description                                      | Formatted |
|--------|------------------|--------------------------------------------------|-----------|
| action | literal[replace] | The type of action, This is always "replace".    | -         |
| files  | list[str]        | The list of files to perform the replacement in. | yes       |
| src    | str              | The source string to be replaced.                | no        |
| dest   | str              | The destination string.                          | yes       |

#### Delete action

Delete actions are used to delete files.

| Field  | Type            | Description                                  | Formatted |
|--------|-----------------|----------------------------------------------|-----------|
| action | literal[delete] | The type of action, This is always "delete". | -         |
| files  | list[str]       | The list of files to delete.                 | yes       |

#### Create action

Create actions are used to create files.

| Field   | Type            | Description                                  | Formatted |
|---------|-----------------|----------------------------------------------|-----------|
| action  | literal[create] | The type of action, This is always "create". | -         |
| files   | str             | The filename to create.                      | yes       |
| content | ?str            | The content of the file.                     | yes       |

#### Rename action

Rename actions are used to rename files.

| Field  | Type            | Description                                  | Formatted |
|--------|-----------------|----------------------------------------------|-----------|
| action | literal[rename] | The type of action, This is always "rename". | -         |
| file   | str             | The file to rename.                          | Yes       |
| dest   | str             | The new filename.                            | Yes       |

#### Copy action

Copy actions are used to copy files.

| Field  | Type          | Description                                                             | Formatted |
|--------|---------------|-------------------------------------------------------------------------|-----------|
| action | literal[copy] | The type of action, This is always "copy".                              | -         |
| file   | str           | The file to copy.                                                       | Yes       |
| dest   | str           | The destination filename. This is formatted with the defined variables. | Yes       |

#### Command Action

Command actions are used to run shell commands. These commands are only run if `--shell` is explicitly specified by the user, or the user has set shell to allow by default using `noo conf set shell allow`.

| Field   | Type               | Description                                                                                                              | Formatted |
|---------|--------------------|--------------------------------------------------------------------------------------------------------------------------|-----------|
| action  | literal[command]   | The type of action, This is always "command".                                                                            | -         |
| command | str                | The command to run.                                                                                                      | yes       |
| fail    | bool; default=true | Whether the whole process should fail if the command returns a non-zero exit code.                                       | -         |
| cwd     | str; default=.     | The working directory for the command. Defaults to the project directory for `clone` or the current directory for `mod`. | no        |

#### Format Action

Format actions format a given file or set of files with the current noo variables.

| Field  | Type            | Description                                  | Formatted |
|--------|-----------------|----------------------------------------------|-----------|
| action | literal[format] | The type of action, This is always "format". | -         |
| files  | list[str]       | The list of files to format.                 | yes       |

#### Read Action

Read actions are used to read a variable from the console suring a step, allowing for dynamically read variables depending on step conditions.

| Field   | Type          | Description                                                           | Formatted |
|---------|---------------|-----------------------------------------------------------------------|-----------|
| action  | literal[read] | The type of action, This is always "read".                            | -         |
| name    | str           | The name of the variable to read.                                     | yes       |
| prompt  | ?str          | The prompt to display. If not provided a prompt is generated by name. | yes       |
| default | ?str          | An optional default value.                                            | yes       |

#### Remote Action

Remote actions are used to run additional modify noofiles in another noofile.

| Field  | Type | Description                                                                  | Formatted |
|--------|------|------------------------------------------------------------------------------|-----------|
| action | str  | The type of action, This is always "remote".                                 | -         |
| remote | str  | The noofile to run. This supports the same refs as `noo clone` and `noo mod` | no        |

### Condition Object

| Field | Type                       | Description                             |
|-------|----------------------------|-----------------------------------------|
| op    | Literal[[OpType](#optype)] | The operation to perform.               |
| var   | str                        | The variable to compare, i.e. noo:year. |
| value | str                        | The value to compare to.                |

#### OpType

List of operation types:

| Name | Operation              |
|------|------------------------|
| eq   | Equals                 |
| ne   | Not Equals             |
| gt   | Greater Than           |
| lt   | Less Than              |
| ge   | Greater Than or Equals |
| le   | Less Than or Equals    |
