from fastapi import FastAPI
from translator import translator
import uvicorn
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel
import logging
from logging.handlers import RotatingFileHandler
from lang_list import langs

logging.basicConfig(
    handlers=[RotatingFileHandler("webserver.log", maxBytes=5_000_000, backupCount=5)],
    encoding="utf-8",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

app = FastAPI()

translator = translator()


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

    for i in langs:
        if i != request.src_lang:
            meta = {
                "src_lang": request.src_lang,
                "tgt_lang": i,
                "input_text": request.input_text,
            }
            print(meta)

            result = translator.translate(**meta)

            translations[i] = result

    result_json = {
        "translations": translations,
    }
    logging.debug(f"Вернулся перевод: {result_json}\n")

    return JSONResponse(content=result_json)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
