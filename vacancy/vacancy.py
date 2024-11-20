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


@app.post("/vacancy/index")
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
                 "content": f"Напиши уникальное индексируемое в google мета-описание не более 200 слов для вакансии компании, опубликованным на международном маркете Mytrade.kz на основе этого текста: «{text}»."}],
            stream=False,
        )
        print(response)

        meta_res = response.strip('"')

        return JSONResponse(content={"meta": meta_res})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/vacancy/seo")
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
                 "content": f"Напиши уникальный seo-текст не более 500 слов о возможности найти на международном сервисе поиска работы Mytrade.kz вакансии «{text}» в различных странах мира, включая Казахстан. Приведи примеры вакансий «{text}». Перечисли кратко несколько городов мира, в которых компании ищут кандидатов на данную вакансию в сервисе поиска работы Mytrade.kz. В тексте не используй заголовки для разделов, не используй слово 'Нур-султан', не используй иконки, не используй переносы строк на новую строку, не используй пункты, не используй жирный шрифт. Текст должен быть полностью слитным."}],
            stream=False,
        )
        print(response)

        meta_res = response.strip('"')

        return JSONResponse(content={"meta": meta_res})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/vacancy/resume/index")
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
                 "content": f" «Напиши уникальное индексируемое в google мета-описание не более 200 слов для резюме соискателя работы, опубликованным на международном маркете Mytrade.kz на основе этого текста: «{text}»."}],
            stream=False,
        )
        print(response)

        meta_res = response.strip('"')

        return JSONResponse(content={"meta": meta_res})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/vacancy/resume/seo")
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
                 "content": f"Напиши уникальный seo-текст не более 500 слов о возможности найти на международном сервисе поиска работы Mytrade.kz резюме кандидатов и соискателей на должность «{text}» в различных странах мира, включая Казахстан. Приведи примеры резюме «{text}». Перечисли кратко несколько городов мира, в которых соискатели ищут работу на должность (вставить полученное от БЭК МТ наименование желаемой должности) в сервисе поиска работы Mytrade.kz. В тексте не используй заголовки для разделов, не используй слово 'Нур-султан', не используй иконки, не используй переносы строк на новую строку, не используй пункты, не используй жирный шрифт. Текст должен быть полностью слитным."}],
            stream=False,
        )
        print(response)

        meta_res = response.strip('"')

        return JSONResponse(content={"meta": meta_res})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
