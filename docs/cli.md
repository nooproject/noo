# CLI

The Noo CLI is how you interact with noo to perform operation such as cloning noofiles, modifying from noofiles, and setting config defaults.

## `clone`

The clone command is used to clone a noofile from a noofile 'ref'.

**Usage:**

    noo clone <dest> <ref> [--shell] [--quiet] [--index<str>]

| Parameter | Description                                                                                                                            |
|-----------|----------------------------------------------------------------------------------------------------------------------------------------|
| dest      | The destination directory to clone the noofile to. This directory must not already exist.                                              |
| ref       | The reference to the noofile to clone. This can be a local file, local registry entry, HTTP(S) URL, or [index identifier](indices.md). |
| --shell   | Enable command actions for this clone.                                                                                                 |
| --quiet   | Only display required output, such as requests for input or errors.                                                                    |
| --index   | The noo file index to use for resolving index references.                                                                              |

## `mod`

The mod command is used to in-place modify an existing project using a noofile.

**Usage:**

    noo mod <ref> [dest=.] [--shell] [--quiet] [--index<str>]

| Parameter | Description                                                                                                                                  |
|-----------|----------------------------------------------------------------------------------------------------------------------------------------------|
| ref       | The reference to the noofile to modify with. This can be a local file, local registry entry, HTTP(S) URL, or [index identifier](indices.md). |
| dest      | The destination directory to modify. Defaults to the current working directory.                                                              |
| --shell   | Enable command actions for this modification.                                                                                                |
| --quiet   | Only display required output, such as requests for input or errors.                                                                          |
| --index   | The noo file index to use for resolving index references.                                                                                    |

## `reg`

The reg subcommand is used to modify local registry entries.

### `add`

The add command is used to add a noofile to the local registry.

**Usage:**

    noo reg add <name> <ref>

| Parameter | Description                                                                                                                               |
|-----------|-------------------------------------------------------------------------------------------------------------------------------------------|
| name      | T                                                                                                                                         |
| ref       | The reference to the noofile to register. This can be a local file, local registry entry, HTTP(S) URL, or [index identifier](indices.md). |

### `remove`

The remove command is used to remove a noofile from the local registry.

**Usage:**

    noo reg remove <name>

| Parameter | Description                               |
|-----------|-------------------------------------------|
| name      | The name of the registry entry to remove. |

## `conf`

The conf subcommand is used to modify the default Noo configuration.

### `set`

The set command is used to set a default value for a configuration option.

**Usage:**

    noo conf set <key> <value>

| Parameter | Description                  |
|-----------|------------------------------|
| key       | The config key to set.       |
| value     | The value to set the key to. |

### `reset`

The reset command is used to reset a default value for a configuration option.

**Usage:**

    noo conf reset <key>

| Parameter | Description              |
|-----------|--------------------------|
| key       | The config key to reset. |

### Valid Keys

| Key   | Description                                                                                           |
|-------|-------------------------------------------------------------------------------------------------------|
| shell | Whether the shell is allowed by default in clone and mod operations. Allowed values: `allow`, `deny`. |
| index | The noo file index to use for resolving index references.                                             |
