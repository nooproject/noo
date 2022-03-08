from textwrap import dedent

from fastapi import FastAPI, Response

app = FastAPI()


@app.get("/")
async def get_project():
    return {
        "type": "static",
        "index": {
            "@vcokltfre/api-template:latest": "https://raw.githubusercontent.com/vcokltfre/noofiles/master/noofiles/api.noofile.yml",
        },
    }
