from openai import OpenAI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from app_create import create_app

load_dotenv()

# Инициализация клиента OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = create_app(create_custom_static_urls=True)

# Модель запроса
class Txt(BaseModel):
    text: str

# Функция для генерации текста через OpenAI
def generate_text_openai(prompt: str):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a professional copywriter who specializes in creating unique, SEO-optimized texts that improve search engine indexing and ranking."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    # Доступ к содержимому через атрибуты
    return response.choices[0].message.content.strip()

# Маршрут FastAPI
@app.post("/vacancy/resume/index")
async def a(request_body: Txt):
    try:
        prompt = f"Напишите уникальное, индексируемое в Google мета-описание (до 200 слов) для резюме, основанное на следующем тексте: {request_body.text}"
        meta_description = generate_text_openai(prompt)
        return JSONResponse(content={"meta": meta_description})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/gpt")
async def b(request_body: Txt):
    try:
        # Формируем запрос для генерации мета-текста
        prompt = f"Создай уникальный мета-текст до 200 символов: {request_body.text}"
        meta_res = generate_text_openai(prompt)
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)



@app.post("/desk/auto/goods/index")
async def c(request_body: Txt):
    try:
        prompt = f"Напиши уникальное индексируемое в google мета-описание не более 200 слов для объявления об авто на международной доске объявлений Mytrade.kz на основе этого текста: «{request_body.text}»."
        meta_res = generate_text_openai(prompt)
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/desk/auto/goods/seo")
async def d(request_body: Txt):
    try:
        prompt = f"Напиши уникальный seo-текст не более 500 слов о возможности найти на международной доске объявлений Mytrade.kz объявления от компаний и частных лиц о продаже, покупки или сдачи в аренду «{request_body.text}». Приведи различные примеры. Перечисли кратко несколько городов мира, в которых можно найти опубликованные объявления на доске объявлений Mytrade.kz о покупке, продаже, аренды авто. В тексте не используй заголовки для разделов, не используй слово 'Нур-султан', не используй иконки, не используй переносы строк на новую строку, не используй пункты, не используй жирный шрифт. Текст должен быть полностью слитным"
        meta_res = generate_text_openai(prompt)
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/desk/auto/categories/index")
async def e(request_body: Txt):
    try:
        prompt = f"Напиши уникальное индексируемое в google мета-описание не более 200 слов для категории международной доски объявлений Mytrade.kz «{request_body.text}». Напиши кратко какие авто можно купить, продать, взять или сдать в аренду в данной категории."
        meta_res = generate_text_openai(prompt)
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/desk/auto/categories/seo")
async def f(request_body: Txt):
    try:
        prompt = f"Напиши уникальный seo-текст из 500 слов о возможности размещения объявлений о продаже, покупки, аренды авто в категории «{request_body.text}» на международной доске объявлений Mytrade.kz. Расскажи о широком ассортименте объявлений в категории «{request_body.text}» от компаний и частных лиц со всего мира. Перечисли кратко и рандомно опубликованные на доске объявлений Mytrade.kz марки и модели авто из категории «{request_body.text}» и приведи примеры их применения. Перечисли кратко несколько городов мира, в которых частные лица и компании продают, покупают или арендуют авто из данной категории на доске объявлений Mytrade.kz. В тексте не используй заголовки для разделов, не используй слово 'Нур-султан', не используй иконки, не используй переносы строк на новую строку, не используй пункты, не используй жирный шрифт. Текст должен быть полностью слитным"
        meta_res = generate_text_openai(prompt)
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/desk/goods/index")
async def g(request_body: Txt):
    try:
        prompt = f"Напиши уникальное индексируемое в google мета-описание не более 200 слов для объявления, опубликованного на международной доске объявлений Mytrade.kz на основе этого текста: {request_body.text}"
        meta_res = generate_text_openai(prompt)
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/desk/goods/seo")
async def h(request_body: Txt):
    try:
        prompt = f"Напиши уникальный seo-текст не более 500 слов о возможности найти на международной доске объявлений Mytrade.kz объявления от компаний и частных лиц о покупке и продаже «{request_body.text}». Приведи примеры применения товара «{request_body.text}». Перечисли кратко несколько городов мира, в которых можно найти этот товар, опубликованный на доске объявлений Mytrade.kz. В тексте не используй заголовки для разделов, не используй слово 'Нур-султан', не используй иконки, не используй переносы строк на новую строку, не используй пункты, не используй жирный шрифт. Текст должен быть полностью слитным."
        meta_res = generate_text_openai(prompt)
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/desk/category/seo")
async def i(request_body: Txt):
    try:
        prompt = f"Напиши уникальный seo-текст из 500 слов о размещении объявлений в категории «{request_body.text}» на международной доске объявлений Mytrade.kz. Расскажи о широком ассортименте объявлений в категории «{request_body.text}» от компаний и частных лиц со всего мира. Перечисли опубликованные на доске объявлений Mytrade.kz товары из категории «{request_body.text}» и приведи примеры их применения. Перечисли кратко несколько городов мира, в которых частные лица и компании продают товары из данной категории на доскне объявлений Mytrade.kz. В тексте не используй заголовки для разделов, не используй слово 'Нур-султан', не используй иконки, не используй переносы строк на новую строку, не используй пункты, не используй жирный шрифт. Текст должен быть полностью слитным"
        meta_res = generate_text_openai(prompt)
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/desk/category/index")
async def j(request_body: Txt):
    try:
        prompt = f"Напиши уникальное индексируемое в google мета-описание не более 200 слов для категории международной доски объявлений Mytrade.kz «{request_body.text}». Напиши кратко какие товары можно купить или продать в данной категории"
        meta_res = generate_text_openai(prompt)
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/desk/realty/goods/index")
async def k(request_body: Txt):
    try:
        prompt = f"Напиши уникальное индексируемое в google мета-описание не более 200 слов для объявления о недвижимости на международной доске объявлений Mytrade.kz на основе этого текста: «{request_body.text}»"
        meta_res = generate_text_openai(prompt)
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/desk/realty/goods/seo")
async def l(request_body: Txt):
    try:
        prompt = f"Напиши уникальный seo-текст не более 500 слов о возможности найти на международной доске объявлений Mytrade.kz объявления от компаний и частных лиц о продаже, покупки или сдачи в аренду «{request_body.text}». Приведи различные примеры. Перечисли кратко несколько городов мира, в которых можно найти опубликованные объявления на доске объявлений Mytrade.kz о покупке, продаже, аренды похожей недвижимости. В тексте не используй заголовки для разделов, не используй слово 'Нур-султан', не используй иконки, не используй переносы строк на новую строку, не используй пункты, не используй жирный шрифт. Текст должен быть полностью слитным"
        meta_res = generate_text_openai(prompt)
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/desk/realty/categories/index")
async def m(request_body: Txt):
    try:
        prompt = f"Напиши уникальное индексируемое в google мета-описание не более 200 слов для категории международной доски объявлений Mytrade.kz «{request_body.text}». Напиши кратко какую недвижимость можно купить, продать, взять или сдать в аренду в данной категории"
        meta_res = generate_text_openai(prompt)
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/desk/realty/categories/seo")
async def n(request_body: Txt):
    try:
        prompt = f"Напиши уникальный seo-текст из 500 слов о возможности размещения объявлений о продаже, покупки, аренды недвижимости в категории «{request_body.text}» на международной доске объявлений Mytrade.kz. Расскажи о большом количестве объявлений в категории «{request_body.text}» от компаний и частных лиц со всего мира. Перечисли кратко и рандомно опубликованные на доске объявлений Mytrade.kz виды недвижимостей из категории «{request_body.text}». Перечисли кратко несколько городов мира, в которых частные лица и компании продают, покупают или сдают в аренду недвижимость из данной категории на доске объявлений Mytrade.kz. В тексте не используй заголовки для разделов, не используй слово 'Нур-султан', не используй иконки, не используй переносы строк на новую строку, не используй пункты, не используй жирный шрифт. Текст должен быть полностью слитным"
        meta_res = generate_text_openai(prompt)
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/desk/services/index")
async def o(request_body: Txt):
    try:
        prompt = f" Напиши уникальное индексируемое в google мета-описание не более 200 слов для объявления про услугу, опубликованного на международной доске объявлений Mytrade.kz на основе этого текста: «{request_body.text}». При генерации ответа не используй ID объявления."
        meta_res = generate_text_openai(prompt)
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/desk/services/seo")
async def p(request_body: Txt):
    try:
        prompt = f"Напиши уникальный seo-текст не более 500 слов о возможности найти на международной доске объявлений Mytrade.kz объявления от компаний и частных лиц об услуге «{request_body.text}». Приведи примеры применения услуги «{request_body.text}». Перечисли кратко несколько городов мира, в которых можно найти эту услугу, опубликованную на доске объявлений Mytrade.kz. В тексте не используй заголовки для разделов, не используй слово 'Нур-султан', не используй иконки, не используй переносы строк на новую строку, не используй пункты, не используй жирный шрифт. Текст должен быть полностью слитным"
        meta_res = generate_text_openai(prompt)
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/desk/categories/index")
async def q(request_body: Txt):
    try:
        prompt = f"Напиши уникальное индексируемое в google мета-описание не более 200 слов для категории международной доски объявлений Mytrade.kz «{request_body.text}». Напиши кратко какие услуги можно купить или предложить купить в данной категории."
        meta_res = generate_text_openai(prompt)
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/desk/categories/seo")
async def r(request_body: Txt):
    try:
        prompt = f"Напиши уникальный seo-текст из 500 слов о размещении объявлений об услугах в категории «{request_body.text}» на международной доске объявлений Mytrade.kz. Расскажи о широком ассортименте объявлений в категории «{request_body.text}» от компаний и частных лиц со всего мира. Перечисли опубликованные на доске объявлений Mytrade.kz услуги из категории «{request_body.text}» и приведи примеры их применения. Перечисли кратко несколько городов мира, в которых частные лица и компании продают товары из данной категории на доске объявлений Mytrade.kz. В тексте не используй заголовки для разделов, не используй слово 'Нур-султан', не используй иконки, не используй переносы строк на новую строку, не используй пункты, не используй жирный шрифт. Текст должен быть полностью слитным"
        meta_res = generate_text_openai(prompt)
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/goods/index")
async def s(request_body: Txt):
    try:
        prompt = f"Напиши уникальное индексируемое в google мета-описание не более 200 слов для товара, продаваемого на международном маркете Mytrade.kz на основе этого текста: {request_body.text}"
        meta_res = generate_text_openai(prompt)
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/goods/seo")
async def t(request_body: Txt):
    try:
        prompt = f"Напиши уникальный seo-текст не более 500 слов о возможности найти на международном маркете Mytrade товар «{request_body.text}» продаваемый магазинами со всего мира, включая Казахстан. Приведи примеры применения товара «{request_body.text}». Перечисли кратко несколько городов мира, в которых магазины продают этот товар в маркете Mytrade.kz. В тексте не используй заголовки для разделов, не используй слово 'Нур-султан', не используй иконки, не используй переносы строк на новую строку, не используй пункты, не используй жирный шрифт. Текст должен быть полностью слитным."
        meta_res = generate_text_openai(prompt)
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/category/seo")
async def u(request_body: Txt):
    try:
        prompt = f"Напиши уникальный seo-текст из 500 слов о продаже товаров из категории «{request_body.text}» на международном маркете Mytrade.kz. Расскажи о широком ассортименте товаров в категории «{request_body.text}» от продавцов и производителей со всего мира. Перечисли продаваемые в маркете Mytrade.kz товары из категории «{request_body.text}» и приведи примеры их применения. Перечисли кратко несколько городов мира, в которых магазины продают товары из данной категории на маркете Mytrade.kz. В тексте не используй заголовки для разделов, не используй слово 'Нур-султан', не используй иконки, не используй переносы строк на новую строку, не используй пункты, не используй жирный шрифт. Текст должен быть полностью слитным"
        meta_res = generate_text_openai(prompt)
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/category/index")
async def v(request_body: Txt):
    try:
        prompt = f"Напиши уникальное индексируемое в google мета-описание не более 200 слов для категории международного маркета Mytrade.kz «{request_body.text}». Напиши кратко какие товары можно купить в данной категории."
        meta_res = generate_text_openai(prompt)
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/vacancy/index")
async def w(request_body: Txt):
    try:
        prompt = f"Напиши уникальное индексируемое в google мета-описание не более 200 слов для вакансии компании, опубликованным на международном маркете Mytrade.kz на основе этого текста: «{request_body.text}»."
        meta_res = generate_text_openai(prompt)
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/vacancy/seo")
async def x(request_body: Txt):
    try:
        prompt = f"Напиши уникальный seo-текст не более 500 слов о возможности найти на международном сервисе поиска работы Mytrade.kz вакансии «{request_body.text}» в различных странах мира, включая Казахстан. Приведи примеры вакансий «{request_body.text}». Перечисли кратко несколько городов мира, в которых компании ищут кандидатов на данную вакансию в сервисе поиска работы Mytrade.kz. В тексте не используй заголовки для разделов, не используй слово 'Нур-султан', не используй иконки, не используй переносы строк на новую строку, не используй пункты, не используй жирный шрифт. Текст должен быть полностью слитным."
        meta_res = generate_text_openai(prompt)
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/vacancy/resume/index")
async def y(request_body: Txt):
    try:
        prompt = f" «Напиши уникальное индексируемое в google мета-описание не более 200 слов для резюме соискателя работы, опубликованным на международном маркете Mytrade.kz на основе этого текста: «{request_body.text}»."
        meta_res = generate_text_openai(prompt)
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/vacancy/resume/seo")
async def z(request_body: Txt):
    try:
        prompt = f"Напиши уникальный seo-текст не более 500 слов о возможности найти на международном сервисе поиска работы Mytrade.kz резюме кандидатов и соискателей на должность «{request_body.text}» в различных странах мира, включая Казахстан. Приведи примеры резюме «{request_body.text}». Перечисли кратко несколько городов мира, в которых соискатели ищут работу на должность (вставить полученное от БЭК МТ наименование желаемой должности) в сервисе поиска работы Mytrade.kz. В тексте не используй заголовки для разделов, не используй слово 'Нур-султан', не используй иконки, не используй переносы строк на новую строку, не используй пункты, не используй жирный шрифт. Текст должен быть полностью слитным."
        meta_res = generate_text_openai(prompt)
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/phys/seo")
async def aa(request_body: Txt):
    try:
        prompt = f"Напиши уникальный seo-текст не более 500 слов о возможности на международной платформе Mytrade.kz смотреть объявления о продаваемых товарах, услугах, недвижимости, автомобилей, мотоциклов, скутеров, спецтехники от частных физических лиц на их личных странницах. А также возможности смотреть об объявленных закупках различных товаров и услуг частными лицами, которые они размещают в своих профилях. Напиши также, что на странницах частных лиц можно добавить в избранные понравившиеся объявления и отправить автору объявления сообщения на удобном языке отправителя. В тексте не используй заголовки для разделов, не используй слово 'Нур-султан', не используй иконки, не используй переносы строк на новую строку, не используй пункты, не используй жирный шрифт. Текст должен быть полностью слитным: {request_body.text}"
        meta_res = generate_text_openai(prompt)
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/phys/index")
async def ab(request_body: Txt):
    try:
        prompt = f"Напиши уникальный индексируемый в google мета-текст не более 200 слов для текста «{request_body.text}». При генерации ответа не используй ID пользователя."
        meta_res = generate_text_openai(prompt)
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/jud/seo")
async def ac(request_body: Txt):
    try:
        prompt = f"Напиши уникальный seo-текст не более 500 слов о возможности найти на международной торговой платформе Mytrade различные товары и услуги от магазинов и компаний со всего мира, включая Казахстан. Приведи примеры продаваемых товаров и услуг от компаний из отрасли «{request_body.text}». Перечисли кратко несколько городов мира, в которых компании продают товары и услуги в маркете и доске объявлений Mytrade.kz. В тексте не используй заголовки для разделов, не используй слово 'Нур-султан', не используй иконки, не используй переносы строк на новую строку, не используй пункты, не используй жирный шрифт. Текст должен быть полностью слитным. "
        meta_res = generate_text_openai(prompt)
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/jud/index")
async def ad(request_body: Txt):
    try:
        prompt = f"Напиши уникальный индексируемый в google мета-текст не более 200 слов для текста: «{request_body.text}»."
        meta_res = generate_text_openai(prompt)
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8020)
