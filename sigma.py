from fastapi import FastAPI
from deep_translator import GoogleTranslator
import uvicorn
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel
import logging
from logging.handlers import RotatingFileHandler

logging.basicConfig(
    handlers=[RotatingFileHandler("sigma.log", maxBytes=5_000_000, backupCount=5)],
    encoding="utf-8",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

lang_mapping = {
    "rus_Cyrl": "ru",
    "uzn_Latn": "uz",
    "nld_Latn": "nl",
    "fra_Latn": "fr",
    "kor_Hang": "ko",
    "ita_Latn": "it",
    "kaz_Cyrl": "kk",
    "eng_Latn": "en",
    "zho_Hans": "zh-CN",
    "arb_Arab": "ar",
    "tur_Latn": "tr",
    "deu_Latn": "de",
    "spa_Latn": "es",
}
langs = list(lang_mapping.keys())

app = FastAPI()

  ### DATA SCHEMA ###


class Request(BaseModel):
    src_lang: str
    input_text: str


  ### API ###

@app.get("/", include_in_schema=False)
async def home():
    return RedirectResponse("/docs")


@app.post("/translate", tags=["translate"])
async def translate(request):
    print(f"Got request: {request}")
    logging.info(f"Got request: {request}\n")
    body = await request.body
    src = body.get('src_lang')
    text = body.get('input_text')
    google_src = lang_mapping.get(src)

    if not google_src:
        return JSONResponse(content={"error": "Unacceptable foreign language."}, status_code=400)

    translations = {}

    for tgt in langs:
        if tgt != src:
            google_tgt = lang_mapping[tgt]
            try:
                result = GoogleTranslator(source=google_src, target=google_tgt).translate(text)
                print(result)
                translations[tgt] = result
            except Exception as e:
                logging.error(f"Error when translating into {google_tgt}: {e}")
                translations[tgt] = "Translating error"

    result_json = {
        "translations": translations,
    }
    print(f"The translation has returned: {result_json}")
    logging.info(f"The translation has returned: {result_json}\n")

    return JSONResponse(content=result_json)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
