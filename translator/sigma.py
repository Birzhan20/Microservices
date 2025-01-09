from deep_translator import GoogleTranslator
import uvicorn
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel
from langs import lang_mapping
from app_create import create_app

langs = list(lang_mapping.keys())

app = create_app(create_custom_static_urls=True)

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

    translations = {}

    for tgt in langs:
        if tgt != src:
            google_tgt = lang_mapping[tgt]
            try:
                result = GoogleTranslator(source=google_src, target=google_tgt).translate(text)
                translations[tgt] = result
            except Exception as e:
                return JSONResponse(
                    content={"error": f"Failed to translate to {tgt}: {str(e)}"},
                    status_code=500
                )

    result_json = {
        "translations": translations,
    }

    return JSONResponse(content=result_json)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
