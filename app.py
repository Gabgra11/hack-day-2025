from flask import Flask, request
from hackday import get_agent_response, load_knowledge_urls

app = Flask(__name__)

@app.route('/knowledge-urls', methods=['POST'])
def add_knowledge_urls():
    urls = request.json.get('urls', [])
    if not urls:
        return {"error": "No URLs provided"}, 400
    else:
        success = load_knowledge_urls(urls)
        if success:
            return {"message": f"Loaded {len(urls)} URLs into the knowledge base."}, 200
        else:
            return {"error": "Failed to load URLs"}, 500
        
@app.route('/agent-response', methods=['POST'])
def agent_response():
    prompt = request.json.get('prompt', '')
    if not prompt:
        return {"error": "No prompt provided"}, 400
    else:
        response = get_agent_response(prompt)
        if response:
            return {"response": response}, 200
        else:
            return {"error": "Failed to get agent response"}, 500