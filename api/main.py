from fastapi import FastAPI
from routers.autorizacoes import router as aa_router

app = FastAPI()


@app.get("/health")
async def health():
    return {"status:" : "ok" }

app.include_router(aa_router)
