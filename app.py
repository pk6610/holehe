from flask import Flask, jsonify
import asyncio
import importlib
import pkgutil
import holehe.modules
from holehe.core import *
from httpx import AsyncClient

app = Flask(__name__)

def get_all_modules():
    modules = []
    for importer, modname, ispkg in pkgutil.walk_packages(
        path=holehe.modules.__path__,
        prefix=holehe.modules.__name__ + '.',
        onerror=lambda x: None
    ):
        module = importlib.import_module(modname)
        for name in dir(module):
            obj = getattr(module, name)
            if callable(obj) and name == modname.split('.')[-1]:
                modules.append(obj)
    return modules

@app.route('/check/<email>')
def check_email(email):
    async def run():
        data = []
        client = AsyncClient()
        for website in get_all_modules():
            try:
                await website(email, client, data)
            except Exception:
                pass
        await client.aclose()
        return data
    results = asyncio.run(run())
    return jsonify(results)

if __name__ == '__main__':
    app.run()
