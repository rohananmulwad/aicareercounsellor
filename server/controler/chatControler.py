from flask import Blueprint,request,render_template,Response
from utils import handleError
from db import getChatData
from middleware.authMiddleware import login_required
from aiModle import Googlellm

aiRouter = Blueprint("aiRouter", __name__, url_prefix="/aiModel")

llmService = Googlellm()#ai model class 

@aiRouter.route("/chat/stream", methodes=["POST"])
@handleError("error during chat")
@login_required
def chat_stream():# this function send's data in chuck to the user
    #user input data
    data = request.get_json()
    message = data.get("message", "").strip()
    if not message:
        raise ValueError("No message provided")
    #finding chat data in database for context
    #fectch usedId
    userId = user["userId"]
    
    #chat history fetch     
    messageVector = llmService.getEmbedding(message)
    chatHistory = getChatData(userId)
    
    contextText=""
    for chat in chatHistory:
        contextText += f"{chat['chatRole']}: {chat['messageData']}\n"
    contextText += f"user: {message}"  # current user message
    
    def generate():
        for chunk in llmService.askGeminiStream(message):
            yield chunk
            
    return Response(generate(), mimetype="text/plain")


