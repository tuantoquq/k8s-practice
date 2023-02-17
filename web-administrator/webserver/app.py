from fastapi import FastAPI, Request, APIRouter
from fastapi.responses import HTMLResponse
from Controller import userController, auditController, minerController
import uvicorn, time
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

app.include_router(userController.router)
app.include_router(auditController.router)
app.include_router(minerController.router)

class SPAStaticFiles(StaticFiles):
	async def get_response(self, path: str, scope):
		response = await super().get_response(path, scope)
		if response.status_code == 404:
			response = await super().get_response('.', scope)
		return response

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", reload=False, log_level="debug", port=int(os.getenv('SERVER_PORT')))