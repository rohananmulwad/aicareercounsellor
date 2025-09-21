from flask import Blueprint, render_template, request, Response, jsonify
from middleware.authMiddleware import loginRequired
from utils.errorHandler import handleError
from aiModle.googlellm import Googlellm
from db.dbQuery import insertQuizData
from langchain_core.prompts import ChatPromptTemplate
import json
import re

quizRouter = Blueprint("quizRouter", __name__, url_prefix="/quiz")
quizLLM = Googlellm()


def json_serializer(obj):
    if isinstance(obj, datetime):
        # Convert datetime objects to a string in ISO 8601 format
        return obj.isoformat()
    raise TypeError(
        f'Object of type {obj.__class__.__name__} is not JSON serializable')


@quizRouter.route("/question", methods=["GET"])
@handleError("error while getting quiz page")
@loginRequired
def quizPage(user):
    prompt = """
    ## Main Prompt:
    You are a career counselor. Generate a career aptitude quiz with 15 questions in JSON format to assess skills and career preferences.

    ## Required JSON Structure:
    ```json
    {
    "title": "Career Aptitude Assessment",
    "description": "Discover your ideal career path",
    "questions": [
        {
        "id": "q1",
        "type": "multiple_choice",
        "category": "analytical",
        "question": "Question text here",
        "options": [
            {"id": "a", "text": "Option 1", "weight": 3},
            {"id": "b", "text": "Option 2", "weight": 1},
            {"id": "c", "text": "Option 3", "weight": 2},
            {"id": "d", "text": "Option 4", "weight": 1}
        ]
        },
        {
        "id": "q2",
        "type": "rating_scale",
        "category": "communication",
        "question": "Question text here",
        "scale": {
            "min": 1,
            "max": 5,
            "labels": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]
        }
        }
    ]
    }
    ```
    ## Requirements:
    **Generate exactly 15 questions:**
    - 10 multiple_choice questions (4 options each, weights 1-3)
    - 5 rating_scale questions (1-5 scale with labels)

    **Categories to cover (2-3 questions each):**
    - `analytical`: Problem-solving, logical thinking
    - `communication`: Speaking, writing, interpersonal skills
    - `creativity`: Innovation, artistic thinking, design
    - `leadership`: Management, decision-making
    - `technical`: Technology, programming, systems
    - `work_environment`: Team vs solo, structure preferences

    **Question Guidelines:**
    - Use workplace scenarios
    - Make options realistic and balanced
    - No obvious "best" answers
    - Keep questions clear and concise
    ## Examples:
    **Multiple Choice:**
    "When solving a work problem, you prefer to:"
    - "Analyze data systematically" (weight: 3 for analytical)
    - "Brainstorm with the team" (weight: 1 for analytical)
    - "Find creative solutions" (weight: 2 for analytical)
    - "Delegate and coordinate" (weight: 1 for analytical)
    **Rating Scale:**
    "I enjoy explaining complex ideas to others"
    Labels: ["Strongly dislike", "Dislike", "Neutral", "Enjoy", "Love it"]
    ## Output:
    Return only valid JSON. Focus on practical, scenario-based questions that help differentiate career paths.
    """

    response_text = "".join(quizLLM.askGeminiStream(data=prompt))

    # Strip code fences if present
    clean_text = re.sub(r"^```(json)?|```$", "",
                        response_text.strip(), flags=re.MULTILINE)
    # Optional: find the first {...} JSON block
    match = re.search(r"\{.*\}", clean_text, re.DOTALL)
    if match:
        clean_text = match.group(0)

    llmData = json.loads(clean_text)
    return render_template("quiz.html", quizLLMData=llmData)


@quizRouter.route("/quizEval", methods=["POST"])
@handleError("error while evaluating quiz page")
@loginRequired
def quizPageEval(user):
    userId = user["userId"]
    data = request.get_json()
    if not data:
        return "NO data recived", 400

    quizEvalPrompt = ChatPromptTemplate.from_messages([
        ("""
                USER PROFILE DATA:
                {data}

                ## Main Prompt:
                
                You are an expert career psychologist and data analyst. I will provide you with a user's completed career aptitude quiz answers along with the original questions. Your task is to analyze their responses and create a comprehensive psychological and professional profile that will serve as context for future AI interactions with this person.
                ## Required Analysis Output:

                Generate a detailed JSON profile following this structure:

                ```json
                    {{
                    "user_profile": {{
                        "assessment_summary": {{
                        "completion_date": "timestamp",
                        "total_questions": 25,
                        "response_consistency": "high|medium|low",
                        "engagement_level": "high|medium|low"
                        }},
                        "cognitive_profile": {{
                        "analytical_thinking": {{
                            "score": 8.5,
                            "percentile": 85,
                            "description": "Detailed analysis of analytical capabilities",
                            "key_indicators": ["specific behaviors observed", "decision patterns"]
                        }},
                        "creativity_index": {{
                            "score": 6.2,
                            "percentile": 62,
                            "description": "Creative thinking and innovation assessment",
                            "key_indicators": ["creative preferences", "innovation approach"]
                        }},
                        "problem_solving_style": "systematic|intuitive|collaborative|research-driven",
                        "learning_preference": "visual|auditory|kinesthetic|reading"
                        }},
                        "personality_traits": {{
                        "leadership_tendency": {{
                            "score": 7.3,
                            "style": "collaborative|authoritative|servant|transformational",
                            "description": "Leadership approach and natural tendencies"
                        }},
                        "communication_style": {{
                            "score": 6.8,
                            "type": "direct|diplomatic|expressive|analytical",
                            "strengths": ["presentation", "written communication"],
                            "development_areas": ["active listening", "difficult conversations"]
                        }},
                        "work_approach": {{
                            "independence_level": "high|medium|low",
                            "structure_preference": "high|medium|low",
                            "risk_tolerance": "high|medium|low",
                            "pace_preference": "fast|steady|deliberate"
                        }},
                        "social_orientation": {{
                            "extroversion_level": 6.5,
                            "team_collaboration": "natural leader|active contributor|supportive member|independent worker",
                            "networking_comfort": "high|medium|low"
                        }}
                        }},
                        "work_preferences": {{
                        "environment": {{
                            "setting": "corporate|startup|remote|hybrid|academic",
                            "team_size": "large teams|small teams|solo work|varies",
                            "formality_level": "formal|casual|flexible"
                        }},
                        "task_preferences": {{
                            "complexity": "high|medium|low",
                            "variety": "high|medium|low",
                            "time_horizon": "short-term|mixed|long-term projects"
                        }},
                        "motivation_drivers": ["achievement","recognition","learning","autonomy","impact","security","creativity"]
                        }},
                        "skill_assessment": {{
                        "technical_aptitude": {{
                            "score": 7.2,
                            "current_level": "beginner|intermediate|advanced",
                            "learning_interest": "high|medium|low",
                            "specific_areas": ["programming", "data analysis", "design tools"]
                        }},
                        "soft_skills": {{
                            "communication": 8.1,
                            "leadership": 6.9,
                            "collaboration": 7.5,
                            "adaptability": 8.3,
                            "emotional_intelligence": 7.8
                        }},
                        "growth_potential": {{
                            "areas_of_strength": ["analytical thinking", "problem solving"],
                            "development_opportunities": ["public speaking", "project management"],
                            "learning_agility": "high|medium|low"
                        }}
                        }},
                        "career_alignment": {{
                        "top_career_categories": [
                            {{
                            "category": "Technology",
                            "match_score": 85,
                            "reasoning": "Strong analytical and technical scores"
                            }},
                            {{
                            "category": "Business Analysis",
                            "match_score": 78,
                            "reasoning": "Combines analytical thinking with communication skills"
                            }}
                        ],
                        "work_style_indicators": {{
                            "decision_making": "data-driven|intuitive|consensus-building|quick",
                            "project_approach": "methodical|agile|creative|collaborative",
                            "stress_response": "thrives under pressure|steady performer|needs structure"
                        }}
                        }},
                        "ai_interaction_context": {{
                        "communication_preferences": {{
                            "detail_level": "comprehensive|moderate|concise",
                            "explanation_style": "technical|practical|conceptual|step-by-step",
                            "feedback_preference": "direct|encouraging|analytical|balanced"
                        }},
                        "learning_context": {{
                            "preferred_formats": ["tutorials", "examples", "theory", "practice"],
                            "complexity_tolerance": "high|medium|low",
                            "pace_preference": "fast|moderate|slow"
                        }},
                        "decision_support_needs": {{
                            "information_depth": "comprehensive|overview|key points",
                            "comparison_style": "detailed analysis|pros/cons|recommendations",
                            "risk_consideration": "detailed|moderate|minimal"
                        }},
                        "motivation_triggers": [
                            "achievement recognition",
                            "learning opportunities",
                            "problem-solving challenges",
                            "career advancement"
                        ]
                        }},
                        "behavioral_insights": {{
                        "strengths_summary": "Key behavioral strengths based on responses",
                        "potential_blind_spots": "Areas that might need attention",
                        "stress_indicators": "How they might respond under pressure",
                        "growth_mindset": "Evidence of adaptability and learning orientation",
                        "collaboration_style": "How they work with others"
                        }}
                    }}
                    }}

                ```

                ## Analysis Instructions:

                ### 1. Score Calculation:
                - Calculate category scores based on question weights and answer patterns
                - Use percentiles based on typical population distributions
                - Identify consistent patterns vs contradictory responses
                - Flag any unusual response patterns that might indicate rushed completion

                ### 2. Pattern Recognition:
                - Look for cross-category correlations (e.g., high analytical + high technical = engineering aptitude)
                - Identify leadership style from multiple leadership-related questions
                - Determine work environment preferences from various workplace scenarios
                - Assess risk tolerance from decision-making questions

                ### 3. Personality Profiling:
                - Extrapolate personality traits from behavioral preferences
                - Identify communication style from team interaction questions
                - Determine learning style from problem-solving approaches
                - Assess social orientation from collaboration preferences

                ### 4. AI Context Generation:
                - Determine how this person prefers to receive information
                - Identify their decision-making style for future recommendations
                - Note their learning preferences for educational content
                - Understand their motivation drivers for engagement strategies

                ### 5. Quality Indicators:
                - **Response Consistency**: Check if similar questions have similar answers
                - **Engagement Level**: Assess thoroughness and thoughtfulness of responses
                - **Profile Coherence**: Ensure the overall profile makes logical sense

                ## Specific Analysis Guidelines:

                1. **Be Nuanced**: Avoid black-and-white categorizations; use ranges and qualifiers
                2. **Evidence-Based**: Every insight should be traceable to specific question responses
                3. **Actionable**: Provide insights that can inform future AI interactions
                4. **Respectful**: Maintain a positive, growth-oriented perspective
                5. **Comprehensive**: Cover cognitive, emotional, and behavioral aspects

                ## Context Application Examples:

                Based on the profile, future AI interactions should:
                - **High Analytical + Low Communication**: Provide detailed technical explanations but offer communication skill development
                - **High Leadership + High Technical**: Suggest management roles in technical fields
                - **Low Risk Tolerance + High Structure**: Recommend stable career paths with clear advancement
                - **High Creativity + Medium Technical**: Suggest design or product roles that blend both skills

                ## Output Requirements:

                1. **Valid JSON**: Ensure proper formatting and escaping
                2. **Complete Scores**: All numerical scores should be on a 1-10 scale
                3. **Clear Descriptions**: Each score should have explanatory text
                4. **Actionable Insights**: Focus on practical implications for career and personal development
                5. **AI Context**: Specifically address how AI should interact with this person in the future

                ## Important Notes:

                - Base all analysis strictly on the provided quiz responses
                - If certain areas lack sufficient data, indicate "insufficient data" rather than guessing
                - Maintain professional, objective language throughout
                - Focus on strengths while acknowledging growth areas constructively
                - Consider cultural and individual differences in interpreting responses""")
    ])
    json_data_str = json.dumps(data, default=json_serializer)
    # Escape braces for str.format()
    json_data_str = json_data_str.replace("{", "{{").replace("}", "}}")

    prompt_text = quizEvalPrompt.format(data=json_data_str)

    chunks = ""
    for chunk in quizLLM.askGeminiStream(data=prompt_text):
        chunks += chunk
    
    # Strip code fences if present
    clean_text = re.sub(r"^```(json)?|```$", "",
                        chunks.strip(), flags=re.MULTILINE)
    # Optional: find the first {...} JSON block
    match = re.search(r"\{.*\}", clean_text, re.DOTALL)
    if match:
        clean_text = match.group(0)

    try:
        user_profile = json.loads(clean_text)
        insertQuizData(userId, user_profile)
    except json.JSONDecodeError as e:
        print("JSON parsing failed:", e)
        return jsonify({"error": "Failed to parse AI response"}), 500

    return jsonify(user_profile)
