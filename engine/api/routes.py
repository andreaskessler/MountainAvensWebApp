from . import api_blueprint
import os
from flask import request, jsonify, Response, stream_with_context, json
from flask import redirect, render_template, send_from_directory, url_for
from flask import session

## import requests
## import sseclient
from engine.services import openai_service, vector_service, lawyer_service
from engine.utils.helper_functions import chunk_text, build_prompt, construct_messages_list

@api_blueprint.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@api_blueprint.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(".", 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@api_blueprint.route('/engine.hello', methods=['POST'])
def hello():
   name = request.form.get('name')

   if name:
       print('Request for MountainAvens received with name=%s' % name)
       return render_template('hello.html', name = name)
   else:
       print('Request MountainAvens received with no name or blank name -- redirecting')
       return redirect(url_for('index'))


@api_blueprint.route('/handle-query', methods=['POST'])
def handle_query():
    question = request.json['question']
    chat_history = request.json['chatHistory']
    
    # Get the most similar chunks from Pinecone
    #context_chunks = pinecone_service.get_most_similar_chunks_for_query(question, PINECONE_INDEX_NAME)
    
    # Build the payload to send to OpenAI
    #headers, data = openai_service.construct_llm_payload(question, context_chunks, chat_history)

    # Send to OpenAI's LLM to generate a completion
    def generate():
        #url = 'https://api.openai.com/v1/chat/completions'
        #response = requests.post(url, headers=headers, data=json.dumps(data), stream=True)
        #client = sseclient.SSEClient(response)
        #for event in client.events():
        #    if event.data != '[DONE]':
        #        try:
        #            text = json.loads(event.data)['choices'][0]['delta']['content']
        #            yield(text)
        #        except:
        #            yield('')
        response = "our smart legal advice here..."
        for c in response:
            yield(c)
    
    # Return the streamed response from the LLM to the frontend
    return Response(stream_with_context(generate()))

""""
@api_blueprint.route('/embed-and-store', methods=['POST'])
def embed_and_store():
    url = request.json['url']
    url_text = scraping_service.scrape_website(url)
    chunks = chunk_text(url_text)
    pinecone_service.embed_chunks_and_upload_to_pinecone(chunks, PINECONE_INDEX_NAME)
    response_json = {
        "message": "Chunks embedded and stored successfully"
    }
    return jsonify(response_json)

@api_blueprint.route('/delete-index', methods=['POST'])
def delete_index():
    pinecone_service.delete_index(PINECONE_INDEX_NAME)
    return jsonify({"message": f"Index {PINECONE_INDEX_NAME} deleted successfully"})
"""