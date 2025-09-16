import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_community.embeddings import GooglePalmEmbeddings
load_dotenv()

#This class is desing to handle all the fucntion realted 
#google gemini,such as sending data to llm of google 
class Googlellm:
    def __init__(self,modelName:str="gemini-2.5-flash"):
        self.apiKey=os.getenv("GOOGLE_API_KEY")
        
        if not self.apiKey:
            raise ValueError("GOOGLE_API_KEY environment variable is not set. Please set it.")

        self.llm=ChatGoogleGenerativeAI(model=modelName)
        self.output_parsers=StrOutputParser()
        self.generic_prompt_template = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant. Provide a concise answer."),
            ("user", "{data}")
        ])
        
        self.embeddingModel = GooglePalmEmbeddings(google_api_key=self.apiKey)
    
    def askGemini(self,data:str)->str:
        """This function send data to googel 
        gemini and wait for output to be back 
        and send it to the back to the client"""
        
        #by creating chain, it automatically parse data and 
        #send's it take no need create extra layer of filter
        
        chain=self.generic_prompt_template|self.llm|self.output_parsers
        response=chain.invoke({"data":data})
        return response
    
    def createRoadMap(self,userData:dict)->str:
        """userData:{
            "userId":123 
            "userName":RandomUser
            "context":"want to explore about ml"
            #to be note the context , is going to be an vector
            which mean's ,the data which is passed on is decode vector data
            let's say 
            userRequest->res=vectorDb(userId,userName)-> return decoed(vector([2,343,34....]))->
            pass_to->data:{userid,userName,res}->createRoadMap(data)->roadmap 
        }"""
        """context could be any thing , it could also be nested"""

        """data/context should be pased into this fcuntion so 
        llm can process it and suggest,
        askGemini and use user vector data to get data
        from db realted to user and will suggest 
        roadmap according to the context"""
        
        roadmapPrompt = ChatPromptTemplate.from_messages([
        ("system", "You are a career guidance expert. Generate a detailed 5-year roadmap based on the following student profile give me that data in roadmap.sh format only point's and nothing more."),
            ("user", """
            Student Profile:
            Interests: {interests}
            Skills: {skills}
            Goal: {goal}
            """)
        ])#it's jsut a genreal&reuseable way of defining prompt
        
        roadmapChain = roadmapPrompt | self.llm | self.output_parsers
        
        response = roadmapChain.invoke({
            "interests": userData.get("interests", "Not specified"),
            "skills": userData.get("skills", "Not specified"),
            "goal": userData.get("goal", "Not specified")
        }) # <- A missing ')' here would cause the error later

        return response
        
        
    def askGeminiStream(self, data: str):
        """streaming version of the code """
        chain = self.generic_prompt_template | self.llm | self.output_parsers
        for chunk in chain.stream({"data": data}):
            yield chunk
            
            
    def getEmbedding(self,text: str):
        """convert strin into vector embedding for semantic search"""
        vector=self.embeddingModel.embed_query(text)
        return vector




if __name__=="__main__":
    try:
        service=Googlellm()
        res1=service.askGemini("what is ml")
        print(res1)
        student_data = {
            "interests": "software development, video games, data visualization",
            "skills": "Python, basic C++, mathematics, problem-solving",
            "goal": "Get a job as a game developer or a backend engineer."
        }
        
        print("--- Generating Career Roadmap ---")
        
        # 3. Call the createRoadMap function with the test data
        roadmap = service.createRoadMap(userData=student_data)
        
        # 4. Print the generated roadmap
        print(roadmap)
    except Exception as e:
        print(e)
