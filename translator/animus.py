import asyncio
from concurrent.futures import ThreadPoolExecutor
from deep_translator import GoogleTranslator
import uvicorn
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from langs import lang_mapping
from app_create import create_app

langs = list(lang_mapping.keys())
app = create_app(create_custom_static_urls=True)

origins = [
    *[f"http://172.20.10.{i}" for i in range(1, 256)],
    *[f"https://172.20.10.{i}" for i in range(1, 256)],
    *[f"https://192.168.0.{i}" for i in range(1, 256)],
    *[f"http://192.168.0.{i}" for i in range(1, 256)],
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

### DATA MODEL ###
class Request(BaseModel):
    src_lang: str
    input_text: str


### API ###
@app.get("/", include_in_schema=False)
async def home():
    return RedirectResponse("/docs")


@app.post("/translate", tags=["translate"])
async def translate(request: Request):
    src = request.src_lang
    text = request.input_text
    google_src = lang_mapping.get(src)

    if not google_src:
        return JSONResponse(content={"error": "Unacceptable foreign language."}, status_code=400)

    def translate_text_sync(tgt):
        """Синхронная функция для перевода текста."""
        google_tgt = lang_mapping.get(tgt)
        try:
            result = GoogleTranslator(source=google_src, target=google_tgt).translate(text)
            return tgt, result
        except Exception as e:
            return tgt, f"Error: {str(e)}"

    # Создаём пул потоков
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        # Создаём задачи для всех языков, кроме исходного
        tasks = [
            loop.run_in_executor(executor, translate_text_sync, tgt)
            for tgt in langs if tgt != src
        ]

        # Выполняем задачи параллельно
        results = await asyncio.gather(*tasks)

    # Формируем словарь переводов
    translations = {tgt: result for tgt, result in results}

    return JSONResponse(content={"translations": translations})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)