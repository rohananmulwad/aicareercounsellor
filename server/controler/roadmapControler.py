from flask import Blueprint, request, Response, render_template, jsonify
from utils.errorHandler import handleError
from db.dbQuery import getChatData,getQuizData
from middleware.authMiddleware import loginRequired
from aiModle import Googlellm
from langchain_core.prompts import ChatPromptTemplate
import json
from datetime import datetime

roadmapRoute = Blueprint("roadmap", __name__, url_prefix="/roadmap")
llmService = Googlellm()


# this function only conver datatime to string or json formate
def json_serializer(obj):
    if isinstance(obj, datetime):
        # Convert datetime objects to a string in ISO 8601 format
        return obj.isoformat()
    raise TypeError(
        f'Object of type {obj.__class__.__name__} is not JSON serializable')


@roadmapRoute.route("/genroadmap", methods=["GET"])
@handleError("roadMapGen", internal_error=1)
@loginRequired
def genRoadMap(user):
    return render_template("roadmap.html")


@roadmapRoute.route("/genroadmapData", methods=["POST"])
@handleError("roadMapError", internal_error=1)
@loginRequired
def genRoadMapData(user):
    userId = user["userId"]
    chatData = getChatData(userId)  # user data isn't going to be cache
    quizData = getQuizData(userId)
    # as it's part of dynamic data
    # as llm depend's on this data whether it's update or not
    # if data is not update then use cache layer and render that smae data or
    # else call llm

    # need to include more data form postgresSql
    # add and retrive more table from db

    if chatData is None and quizData is None:
        chatData = {}
        quizData = {}

    # this message variable is prompt
    # this pice of will pass data and prompt
    # to Google llm and genreate html and later render
    # into another html which is waiting for this html code
    # the whole code is a roadmap genreated based on userdata

    roadmapPrompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert career guidance counselor. Your task is to generate a JSON object containing data for an interactive career roadmap based on user data. Your response must be a valid JSON object and nothing else.

    CRITICAL REQUIREMENTS:
    - The output must be a single JSON object.
    - DO NOT include any text, markdown, or code outside of the JSON object.
    - Generate realistic, actionable career progression content based on the user's profile."""),

        ("user", """Create a career roadmap with the following specifications:

    USER PROFILE DATA:
    {userData}

    OUTPUT FORMAT:
    Generate a JSON object that strictly follows this structure:

        {{
            "lanes": [
                {{
                    "title": "Lane Title",
                    "cards": [
                        {{
                            "id": "card-1",
                            "title": "Skill Name",
                            "description": "Brief description",
                            "timeEstimate": "2-4 weeks",
                            "difficulty": "Beginner|Intermediate|Advanced",
                            "detailedDescription": "Comprehensive explanation of what this skill involves...",
                            "resources": [
                                {{ "title": "Resource Name", "url": "https://example.com",
                                    "type": "Course|Book|Documentation" }}
                            ],
                            "prerequisites": ["Skill A", "Skill B"]
                        }}
                    ]
                }}
            ]
        }}
    ROADMAP STRUCTURE:
    Based on the user profile, create 3-5 career progression lanes. Each lane should contain 4-8 skill cards relevant to progressing from the user's current role to their target career goal.

    CONTENT GENERATION GUIDELINES:
    - Make skill progressions logical and realistic for the user's career path.
    - Include a mix of technical skills, soft skills, and domain knowledge appropriate to their field.
    - Provide 3-5 quality resources per card (mix of free and premium options).
    - Time estimates should be realistic (1-12 weeks per skill).
    - Ensure prerequisite relationships make sense.
    - Tailor difficulty levels to the user's current experience level.

    IMPORTANT NOTES:
    - Analyze the user data carefully to create a truly personalized roadmap.
    - If user data is incomplete, make reasonable assumptions but keep content generic enough to be broadly applicable.
    - Focus on creating a progression that logically builds from their current skills to their career goals.
    - Include both technical and soft skills appropriate to their target role.
    - Make the time estimates and difficulty levels realistic and encouraging.

    Generate the complete JSON object now.""")
    ])
    
    combineUserdata = [chatData, quizData]
    prompt_text = roadmapPrompt.format(
        userData=json.dumps(combineUserdata, default=json_serializer))
    chunks = ""
    for chunk in llmService.askGeminiStream(data=prompt_text):
        chunks += chunk

    #this whole code below is used to fliter json data for frontend
    cleaned_chunks = chunks.strip()
    
    # Remove ```json and ``` if present
    if cleaned_chunks.startswith('```json'):
        cleaned_chunks = cleaned_chunks[7:]  # Remove ```json
    elif cleaned_chunks.startswith('```'):
        cleaned_chunks = cleaned_chunks[3:]   # Remove ```
    
    if cleaned_chunks.endswith('```'):
        cleaned_chunks = cleaned_chunks[:-3]  # Remove closing ```
    
    cleaned_chunks = cleaned_chunks.strip()
    
    # Parse the complete response as JSON
    try:
        res = json.loads(cleaned_chunks)
        return jsonify(res)
    except json.JSONDecodeError as e:
        return jsonify({
            "error": "Failed to parse JSON response", 
            "details": str(e),
            "raw_response": cleaned_chunks[:500]  # First 500 chars for debugging
        }), 500