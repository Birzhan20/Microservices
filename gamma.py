import queue
import threading

from fastapi import FastAPI
from translator_parent import translator
import uvicorn
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel
import logging
from logging.handlers import RotatingFileHandler
from lang_list import langs
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(
    handlers=[RotatingFileHandler("webserver.log", maxBytes=5_000_000, backupCount=5)],
    encoding="utf-8",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


app = FastAPI()

translator = translator()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить все домены (или укажите конкретные домены)
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы
    allow_headers=["*"],  # Разрешить все заголовки
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
    logging.info(f"Получен request: {request}\n")

    translations = {}
    threads = []
    result_queue = queue.Queue()

    def translate_task(tgt_lang):
        meta = {
            "src_lang": request.src_lang,
            "tgt_lang": tgt_lang,
            "input_text": request.input_text,
        }
        print(meta)

        result = translator.translate(**meta)
        result_queue.put((tgt_lang, result))

    for lang in langs:
        if lang != request.src_lang:
            thread = threading.Thread(target=translate_task, args=(lang,))
            threads.append(thread)
            thread.start()

    for thread in threads:
        thread.join()

    while not result_queue.empty():
        tgt_lang, result = result_queue.get()
        translations[tgt_lang] = result

    result_json = {
        "translations": translations,
    }
    logging.debug(f"Вернулся перевод: {result_json}\n")

    return JSONResponse(content=result_json)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
