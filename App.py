from flask import Flask, jsonify
import asyncio
import holehe.modules as modules
from holehe.core import *

app = Flask(__name__)

@app.route('/check/<email>')
async def check_email(email):
    results = []
    client = AsyncClient()
    websites = get_functions()
    for website in websites:
        result = await website(email, client, results)
    await client.aclose()
    return jsonify(results)

if __name__ == '__main__':
    app.run()
