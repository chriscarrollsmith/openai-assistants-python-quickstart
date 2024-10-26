import logging
import dotenv
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


logger = logging.getLogger("uvicorn.error")

dotenv.load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Optional startup logic
    yield
    # Optional shutdown logic


app = FastAPI(lifespan=lifespan)

# Mount static files (e.g., CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def read_home(
):
    categories = {
        "Basic chat": "basic-chat",
        "File search": "file-search",
        "Function calling": "function-calling",
        "All": "all",
    }
    return templates.TemplateResponse("index.html", {"categories": categories})


@app.get("/file-search")
async def read_file_search(
):
    return templates.TemplateResponse("file-search.html")


@app.get("/function-calling")
async def read_function_calling():
    # Define the condition class map
    conditionClassMap = {
        "Cloudy": "weatherBGCloudy",
        "Sunny": "weatherBGSunny",
        "Rainy": "weatherBGRainy",
        "Snowy": "weatherBGSnowy",
        "Windy": "weatherBGWindy",
    }
    
    # Set default values for the weather widget
    location = "---"
    temperature = "---"
    conditions = "Sunny"
    isEmpty = True

    # Pass all necessary context variables to the template
    return templates.TemplateResponse(
        "function-calling.html", 
        {
            "conditionClassMap": conditionClassMap,
            "location": location,
            "temperature": temperature,
            "conditions": conditions,
            "isEmpty": isEmpty
        }
    )


@app.get("/all")
async def read_all(
):
    return templates.TemplateResponse("all.html")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
