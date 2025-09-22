from flask import Blueprint, request, render_template, Response
from utils import handleError
from db import getChatDataByEmbedding, insertChatData
from middleware.authMiddleware import loginRequired
from aiModle import Googlellm

aiRouter = Blueprint("aiRouter", __name__, url_prefix="/aiModel")

llmService = Googlellm()  # ai model class

#redis/cache layer can be used where their are db calls and other llm stuff such as vecotr gen 

@aiRouter.route("/chat", methods=["GET", "POST"])
@handleError("error during chat")
@loginRequired
def chatStream(user):
    # this function need's optimization
    # such as integrate redis, so db call's are less
    # this function send's data in chuck to the user
    # user input data
    if request.method == "GET":
        return render_template("chat.html")
    elif request.method == "POST":
        data = request.get_json()
        message = data.get("message", "").strip()
        if not message:
            raise ValueError("No message provided")

        # finding chat data in database for context
        # fectch usedId

        userId = user["userId"]

        #getting message vector
        messageVector = llmService.getEmbedding(message)
        messageVectorStr = "[" + ",".join(str(x) for x in messageVector) + "]"
        # chat history fetch using vector
        chatHistory = getChatDataByEmbedding(userId, messageVector=messageVectorStr)
        if chatHistory is None:
            chatHistory = []
        contextText = ""
        
        
        for chat in chatHistory:
             contextText += f"{chat[2]}: {chat[0]}\n"
        
        contextText += f"user: {message}"  # current user message

        def generate():
            """this function is need to be more optimize
            as it just add's strem data into local buffer
            integrate redis here and save data their 
            after few time's save all data in db in batch"""

            chunks = []
            for chunk in llmService.askGeminiStream(message):
                chunks.append(chunk)
                yield chunk

            responseText = "".join(chunks)
            rows = [(userId, message, messageVector, "user"),
                    (userId, responseText, llmService.getEmbedding(responseText),
                    "assistant")]
            insertChatData(rows)

        return Response(generate(), mimetype="text/plain")
