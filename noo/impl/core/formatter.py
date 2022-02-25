from __future__ import annotations

from re import compile

VAR = compile(r"\$\$(?P<namespace>[a-zA-Z_]+):(?P<name>[a-zA-Z_]+)")


def replace(text: str, src: str, dest: str, variables: dict[str, dict[str, str | int]]) -> str:
    resolved_dest = dest

    for ns, var in VAR.findall(dest):
        if ns not in ("noo", "var"):
            raise ValueError(f"Unknown namespace: {ns}")

        if var not in variables[ns]:
            raise ValueError(f"Unknown variable: {ns}:{var}")

        resolved_dest = resolved_dest.replace(f"$${ns}:{var}", str(variables[ns][var]))

    return text.replace(src, resolved_dest)


def format_vars(text: str, variables: dict[str, dict[str, str | int]]) -> str:
    for ns, var in VAR.findall(text):
        if ns not in ("noo", "var"):
            raise ValueError(f"Unknown namespace: {ns}")

        if var not in variables[ns]:
            raise ValueError(f"Unknown variable: {ns}:{var}")

        text = text.replace(f"$${ns}:{var}", str(variables[ns][var]))

    return text
