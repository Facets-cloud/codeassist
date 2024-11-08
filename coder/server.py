from flask import Flask, request, jsonify
from pymongo import MongoClient, DESCENDING
import uuid
import os
from datetime import datetime

app = Flask(__name__)

# Environment variable for MongoDB connection string
mongo_connection_string = os.environ.get('MONGO_CONNECTION_STRING', 'mongodb://localhost:27017/')

# Connect to MongoDB
client = MongoClient(mongo_connection_string)
db = client.chat_database
messages_collection = db.messages

@app.route('/agent/start_chat', methods=['POST'])
def start_chat():
    # Start a new chat session and return a thread_id
    thread_id = str(uuid.uuid4())
    return jsonify({'thread_id': thread_id})

@app.route('/agent/continue_chat/<thread_id>', methods=['POST'])
def continue_chat(thread_id):
    # Continue an existing chat
    data = request.json
    message = data.get('message')

    if not message:
        return jsonify({'error': 'Message cannot be empty'}), 400

    # Store the message from the user
    user_message = {
        'thread_id': thread_id,
        'message': message,
        'type': 'user',
        'timestamp': datetime.utcnow()
    }
    messages_collection.insert_one(user_message)

    # Create a stub response
    response_message = "This is a stub for agent interaction."
    agent_message = {
        'thread_id': thread_id,
        'message': response_message,
        'type': 'agent',
        'timestamp': datetime.utcnow()
    }
    messages_collection.insert_one(agent_message)

    return jsonify({'response': response_message})

@app.route('/agent/chat_history/<thread_id>', methods=['GET'])
def get_chat_history(thread_id):
    # Get chat history with pagination
    try:
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 10))
    except ValueError:
        return jsonify({'error': 'Page and page_size must be integers'}), 400

    total_messages = messages_collection.count_documents({'thread_id': thread_id})
    messages_cursor = messages_collection.find({'thread_id': thread_id}).sort('timestamp', DESCENDING).skip((page - 1) * page_size).limit(page_size)
    paginated_messages = list(messages_cursor)

    return jsonify({
        'chat_history': paginated_messages,
        'pagination': {
            'page': page,
            'page_size': page_size,
            'total_messages': total_messages
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
