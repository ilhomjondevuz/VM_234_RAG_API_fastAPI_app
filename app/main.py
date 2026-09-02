from environs import Env
from fastapi import FastAPI

env = Env()
env.read_env()

app = FastAPI(
    title=env.str('APP_NAME'),
    version=env.str('APP_VERSION'),
    description=(
        "O‘zbekiston Respublikasi Vazirlar Mahkamasining "
        "234-son qarori asosida savollarga javob beruvchi RAG API"
    )
)

@app.get("/health")
async def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "VM 234 RAG API",
    }