# File Indices

Noofile indices (for example the official Noo index) are used to host noofiles remotely. These noofiles can be accessed in noo using a ref of the following format:

`@[author/]name[:version]`

| Field   | Description                                                                                                                              |
|---------|------------------------------------------------------------------------------------------------------------------------------------------|
| author  | The author of the noofile. This is optional, files with no author are maintainer by the Noo team.                                        |
| name    | The name of the noofile.                                                                                                                 |
| version | The version of the noofile. This is optional and defaults to `latest`. All non-`latest` values for this are indefinitely cached locally. |

!!! warning

    For package indices like NPM you might have a package like `@vcokltfre/thing` or `thing`, but you should note that in Noo the `@` is **required** for files on indices since the `@` explicitly tells the resolver to look for it on an index rather than in a local registry.

For example:

- `@vcokltfre/api-template`
- `@vcokltfre/api-template:1.0.0`
- `@vcokltfre/api-template:latest`
- `@noo-plugin`
- `@noo-plugin:2.0.0`
- `@noo-plugin:latest`

The default index for Noo is hosted at `https://index.nooproject.dev/api/v1`.

## Types of noofile index

!!! note

    The base URL for both static and dynamic indices must be a JSON object with the key `type` equal to one of `static` and `dynamic`. Noo will use thie field to determine whether it should use the downloaded file as the index (in the case of a static index), or whether to follow the API specification for a dynamic index.

### Static

Static indices are a single static file served from a remote address. This is a JSON file containing a registry of remote noofile refs. Such an index may have a URL like `https://my.site/noo/index.json`. This file should be returned with the response header `Content-Type` set to `application/json`.

Example static index content:

```json
{
  "type": "static",
  "index": {
    "vcokltfre": {
      "api-template": {
        "latest": "https://raw.githubusercontent.com/vcokltfre/noofiles/master/noofiles/api.noofile.yml",
        "1.0.0": "https://raw.githubusercontent.com/vcokltfre/noofiles/master/noofiles/api.noofile.yml"
      }
    }
  }
}
```

Static indices are cached locally for a period of 24 hours. This cache can be force-updated by running `noo index update [index_url]`.

### Dynamic

Dynamic indices are full APIs which follow the below specification for resolving noofiles. They are more similar to package indices such as NPM or PyPI.
