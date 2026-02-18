from dotenv import load_dotenv
import uvicorn
from fastapi import FastAPI, Depends
import os
from otelpy import provider
import logging

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
load_dotenv()

from routes import ( stress_router )

class OtelpyAPI():
    
    def __init__(self):
        self.app = FastAPI(
            title="OtelPy Test",
            version="0.0.1",
            description="OTelPy Test",
            docs_url=f"{os.environ['SERVICE_ROOT_PATH']}/docs/",
            openapi_url=f"{os.environ['SERVICE_ROOT_PATH']}/openapi.json",
            swagger_ui_parameters = {"docExpansion":"none"},
        )
        self.app.router.redirect_slashes = False

        if provider is not None:
            FastAPIInstrumentor.instrument_app(self.app, tracer_provider=provider)

        
        @self.app.get(f"{os.environ['SERVICE_ROOT_PATH']}/")
        async def home():
            return {
                "title": self.app.title,
                "version": self.app.version,
                "description": self.app.description,
            }
        
        @self.app.get(f"{os.environ['SERVICE_ROOT_PATH']}/health", tags=['utils'])
        async def health():
            return {"health": "OK"}
        
        # Using FastAPI instance
        @self.app.get(f"{os.environ['SERVICE_ROOT_PATH']}/url-list", tags=['utils'])
        async def get_all_urls():
            url_list = [{"path": route.path, "name": route.name} 
                        for route in self.app.routes]
            return url_list
        

genai_api = OtelpyAPI()
app = genai_api.app

app.include_router(stress_router)

if __name__ == "__main__":
    
    uvicorn.run(
        app,
        host=os.environ['SERVICE_HOST'],
        port=int(os.environ['SERVICE_PORT']),
        log_level=logging.DEBUG
    )