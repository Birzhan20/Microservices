import nest_asyncio
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
import g4f

nest_asyncio.apply()

app = FastAPI()


class Txt(BaseModel):
    text: str | int


@app.post("/desk/categories/index")
async def generate_meta_description(request_body: Txt):
    text = request_body.text
    print(text)

    if not text:
        return JSONResponse(content={"error": "No input text provided"}, status_code=400)

    try:
        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user",
                "content": f"Напиши уникальное индексируемое в google мета-описание не более 200 слов для категории международной доски объявлений Mytrade.kz «{text}». Напиши кратко какие услуги можно купить или предложить купить в данной категории."}],
            stream=False,
        )
        print(response)

        meta_res = response.strip('"')

        return JSONResponse(content={"meta": meta_res})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/desk/categories/seo")
async def generate_meta_description(request_body: Txt):
    text = request_body.text
    print(text)

    if not text:
        return JSONResponse(content={"error": "No input text provided"}, status_code=400)

    try:
        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user",
                "content": f"Напиши уникальный seo-текст из 500 слов о размещении объявлений об услугах в категории «{text}» на международной доске объявлений Mytrade.kz. Расскажи о широком ассортименте объявлений в категории «{text}» от компаний и частных лиц со всего мира. Перечисли опубликованные на доске объявлений Mytrade.kz услуги из категории «{text}» и приведи примеры их применения. Перечисли кратко несколько городов мира, в которых частные лица и компании продают товары из данной категории на доске объявлений Mytrade.kz. В тексте не используй заголовки для разделов, не используй слово 'Нур-султан', не используй иконки, не используй переносы строк на новую строку, не используй пункты, не используй жирный шрифт. Текст должен быть полностью слитным"}],
            stream=False,
        )
        print(response)

        meta_res = response.strip('"')

        return JSONResponse(content={"meta": meta_res})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
