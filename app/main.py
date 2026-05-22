from pathlib import Path
import sys

from fastapi import FastAPI

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from api.chat import router
app = FastAPI()

app.include_router(
router,
prefix="/api"
)