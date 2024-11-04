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


@app.post("/phys/seo")
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
                "content": f"Напиши уникальный seo-текст не более 500 слов о возможности на международной платформе Mytrade.kz смотреть объявления о продаваемых товарах, услугах, недвижимости, автомобилей, мотоциклов, скутеров, спецтехники от частных физических лиц на их личных странницах. А также возможности смотреть об объявленных закупках различных товаров и услуг частными лицами, которые они размещают в своих профилях. Напиши также, что на странницах частных лиц можно добавить в избранные понравившиеся объявления и отправить автору объявления сообщения на удобном языке отправителя. В тексте не используй заголовки для разделов, не используй слово 'Нур-султан', не используй иконки, не используй переносы строк на новую строку, не используй пункты, не используй жирный шрифт. Текст должен быть полностью слитным: {text}"}],
            stream=False,
        )
        print(response)

        meta_res = response.strip('"')

        return JSONResponse(content={"meta": meta_res})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/phys/index")
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
                "content": f"Напиши уникальный индексируемый в google мета-текст не более 200 слов для текста «{text}». При генерации ответа не используй ID пользователя."}],
            stream=False,
        )
        print(response)

        meta_res = response.strip('"')

        return JSONResponse(content={"meta": meta_res})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
