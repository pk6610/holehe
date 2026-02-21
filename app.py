from flask import Flask, jsonify
import asyncio
from holehe.core import *
from httpx import AsyncClient

app = Flask(__name__)

@app.route('/check/<email>')
def check_email(email):
    async def run():
        data = []
        client = AsyncClient()
        websites = get_functions()
        for website in websites:
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
