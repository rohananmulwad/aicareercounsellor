from .userControler import userRouter
from .chatControler import aiRouter
from .roadmapControler import roadmapRoute

allControllers = [userRouter, aiRouter, roadmapRoute]