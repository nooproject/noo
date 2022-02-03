from re import compile

VAR = compile(r"\$\$(?P<namespace>[a-zA-Z_]+):(?P<name>[a-zA-Z_]+)")


def replace(
    text: str, src: str, dest: str, variables: dict[str, dict[str, str]]
) -> str:
    resolved_dest = dest

    for ns, var in VAR.findall(dest):
        if ns not in ("noo", "var"):
            raise ValueError(f"Unknown namespace: {ns}")

        if var not in variables[ns]:
            raise ValueError(f"Unknown variable: {ns}:{var}")

        resolved_dest = resolved_dest.replace(f"$${ns}:{var}", variables[ns][var])

    return text.replace(src, resolved_dest)
