from .userControler import userRouter
from .chatControler import aiRouter
from .roadmapControler import roadmapRoute
from .quizControler import quizRouter

allControllers = [userRouter, aiRouter, roadmapRoute, quizRouter]