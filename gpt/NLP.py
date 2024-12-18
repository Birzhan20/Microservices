import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from functools import lru_cache

app = FastAPI()

model_name = "OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="cpu",
    torch_dtype=torch.float16
)

torch.set_num_threads(30)
torch.set_num_interop_threads(30)

@lru_cache()
def encode_prompt(prompt):
    return tokenizer(prompt, return_tensors="pt", truncation=True)

def generate_text(prompt):
    inputs = encode_prompt(prompt)
    outputs = model.generate(
        inputs.input_ids,
        temperature=0.7,
        top_p=0.9,
        num_beams=1,
        do_sample=True,
        early_stopping=True,
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

class Txt(BaseModel):
    text: str

@app.post("/gpt")
async def generate_meta_description(request_body: Txt):
    try:
        meta_res = generate_text(f"Создай уникальный мета-текст до 200 символов: {request_body.text}")
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/desk/auto/goods/index")
async def generate_meta_description(request_body: Txt):
    try:
        meta_res = generate_text(f"Напиши уникальное индексируемое в google мета-описание не более 200 слов для объявления об авто на международной доске объявлений Mytrade.kz на основе этого текста: «{request_body.text}».")
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/desk/auto/goods/seo")
async def generate_meta_description(request_body: Txt):
    try:
        meta_res = generate_text(f"Напиши уникальный seo-текст не более 500 слов о возможности найти на международной доске объявлений Mytrade.kz объявления от компаний и частных лиц о продаже, покупки или сдачи в аренду «{request_body.text}». Приведи различные примеры. Перечисли кратко несколько городов мира, в которых можно найти опубликованные объявления на доске объявлений Mytrade.kz о покупке, продаже, аренды авто. В тексте не используй заголовки для разделов, не используй слово 'Нур-султан', не используй иконки, не используй переносы строк на новую строку, не используй пункты, не используй жирный шрифт. Текст должен быть полностью слитным")
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/desk/auto/categories/index")
async def generate_meta_description(request_body: Txt):
    try:
        meta_res = generate_text(f"Напиши уникальное индексируемое в google мета-описание не более 200 слов для категории международной доски объявлений Mytrade.kz «{request_body.text}». Напиши кратко какие авто можно купить, продать, взять или сдать в аренду в данной категории.")
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/desk/auto/categories/seo")
async def generate_meta_description(request_body: Txt):
    try:
        meta_res = generate_text(f"Напиши уникальный seo-текст из 500 слов о возможности размещения объявлений о продаже, покупки, аренды авто в категории «{request_body.text}» на международной доске объявлений Mytrade.kz. Расскажи о широком ассортименте объявлений в категории «{request_body.text}» от компаний и частных лиц со всего мира. Перечисли кратко и рандомно опубликованные на доске объявлений Mytrade.kz марки и модели авто из категории «{request_body.text}» и приведи примеры их применения. Перечисли кратко несколько городов мира, в которых частные лица и компании продают, покупают или арендуют авто из данной категории на доске объявлений Mytrade.kz. В тексте не используй заголовки для разделов, не используй слово 'Нур-султан', не используй иконки, не используй переносы строк на новую строку, не используй пункты, не используй жирный шрифт. Текст должен быть полностью слитным")
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/desk/goods/index")
async def generate_meta_description(request_body: Txt):
    try:
        meta_res = generate_text(f"Напиши уникальное индексируемое в google мета-описание не более 200 слов для объявления, опубликованного на международной доске объявлений Mytrade.kz на основе этого текста: {request_body.text}")
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/desk/goods/seo")
async def generate_meta_description(request_body: Txt):
    try:
        meta_res = generate_text(f"Напиши уникальный seo-текст не более 500 слов о возможности найти на международной доске объявлений Mytrade.kz объявления от компаний и частных лиц о покупке и продаже «{request_body.text}». Приведи примеры применения товара «{request_body.text}». Перечисли кратко несколько городов мира, в которых можно найти этот товар, опубликованный на доске объявлений Mytrade.kz. В тексте не используй заголовки для разделов, не используй слово 'Нур-султан', не используй иконки, не используй переносы строк на новую строку, не используй пункты, не используй жирный шрифт. Текст должен быть полностью слитным.")
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/desk/category/seo")
async def generate_meta_description(request_body: Txt):
    try:
        meta_res = generate_text(f"Напиши уникальный seo-текст из 500 слов о размещении объявлений в категории «{request_body.text}» на международной доске объявлений Mytrade.kz. Расскажи о широком ассортименте объявлений в категории «{request_body.text}» от компаний и частных лиц со всего мира. Перечисли опубликованные на доске объявлений Mytrade.kz товары из категории «{request_body.text}» и приведи примеры их применения. Перечисли кратко несколько городов мира, в которых частные лица и компании продают товары из данной категории на доскне объявлений Mytrade.kz. В тексте не используй заголовки для разделов, не используй слово 'Нур-султан', не используй иконки, не используй переносы строк на новую строку, не используй пункты, не используй жирный шрифт. Текст должен быть полностью слитным")
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/desk/category/index")
async def generate_meta_description(request_body: Txt):
    try:
        meta_res = generate_text(f"Напиши уникальное индексируемое в google мета-описание не более 200 слов для категории международной доски объявлений Mytrade.kz «{request_body.text}». Напиши кратко какие товары можно купить или продать в данной категории")
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/desk/realty/goods/index")
async def generate_meta_description(request_body: Txt):
    try:
        meta_res = generate_text(f"Напиши уникальное индексируемое в google мета-описание не более 200 слов для объявления о недвижимости на международной доске объявлений Mytrade.kz на основе этого текста: «{request_body.text}»")
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/desk/realty/goods/seo")
async def generate_meta_description(request_body: Txt):
    try:
        meta_res = generate_text(f"Напиши уникальный seo-текст не более 500 слов о возможности найти на международной доске объявлений Mytrade.kz объявления от компаний и частных лиц о продаже, покупки или сдачи в аренду «{request_body.text}». Приведи различные примеры. Перечисли кратко несколько городов мира, в которых можно найти опубликованные объявления на доске объявлений Mytrade.kz о покупке, продаже, аренды похожей недвижимости. В тексте не используй заголовки для разделов, не используй слово 'Нур-султан', не используй иконки, не используй переносы строк на новую строку, не используй пункты, не используй жирный шрифт. Текст должен быть полностью слитным")
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/desk/realty/categories/index")
async def generate_meta_description(request_body: Txt):
    try:
        meta_res = generate_text(f"Напиши уникальное индексируемое в google мета-описание не более 200 слов для категории международной доски объявлений Mytrade.kz «{request_body.text}». Напиши кратко какую недвижимость можно купить, продать, взять или сдать в аренду в данной категории")
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/desk/realty/categories/seo")
async def generate_meta_description(request_body: Txt):
    try:
        meta_res = generate_text(f"Напиши уникальный seo-текст из 500 слов о возможности размещения объявлений о продаже, покупки, аренды недвижимости в категории «{request_body.text}» на международной доске объявлений Mytrade.kz. Расскажи о большом количестве объявлений в категории «{request_body.text}» от компаний и частных лиц со всего мира. Перечисли кратко и рандомно опубликованные на доске объявлений Mytrade.kz виды недвижимостей из категории «{request_body.text}». Перечисли кратко несколько городов мира, в которых частные лица и компании продают, покупают или сдают в аренду недвижимость из данной категории на доске объявлений Mytrade.kz. В тексте не используй заголовки для разделов, не используй слово 'Нур-султан', не используй иконки, не используй переносы строк на новую строку, не используй пункты, не используй жирный шрифт. Текст должен быть полностью слитным")
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/desk/services/index")
async def generate_meta_description(request_body: Txt):
    try:
        meta_res = generate_text(f" Напиши уникальное индексируемое в google мета-описание не более 200 слов для объявления про услугу, опубликованного на международной доске объявлений Mytrade.kz на основе этого текста: «{request_body.text}». При генерации ответа не используй ID объявления.")
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/desk/services/seo")
async def generate_meta_description(request_body: Txt):
    try:
        meta_res = generate_text(f"Напиши уникальный seo-текст не более 500 слов о возможности найти на международной доске объявлений Mytrade.kz объявления от компаний и частных лиц об услуге «{request_body.text}». Приведи примеры применения услуги «{request_body.text}». Перечисли кратко несколько городов мира, в которых можно найти эту услугу, опубликованную на доске объявлений Mytrade.kz. В тексте не используй заголовки для разделов, не используй слово 'Нур-султан', не используй иконки, не используй переносы строк на новую строку, не используй пункты, не используй жирный шрифт. Текст должен быть полностью слитным")
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/desk/categories/index")
async def generate_meta_description(request_body: Txt):
    try:
        meta_res = generate_text(f"Напиши уникальное индексируемое в google мета-описание не более 200 слов для категории международной доски объявлений Mytrade.kz «{request_body.text}». Напиши кратко какие услуги можно купить или предложить купить в данной категории.")
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/desk/categories/seo")
async def generate_meta_description(request_body: Txt):
    try:
        meta_res = generate_text(f"Напиши уникальный seo-текст из 500 слов о размещении объявлений об услугах в категории «{request_body.text}» на международной доске объявлений Mytrade.kz. Расскажи о широком ассортименте объявлений в категории «{request_body.text}» от компаний и частных лиц со всего мира. Перечисли опубликованные на доске объявлений Mytrade.kz услуги из категории «{request_body.text}» и приведи примеры их применения. Перечисли кратко несколько городов мира, в которых частные лица и компании продают товары из данной категории на доске объявлений Mytrade.kz. В тексте не используй заголовки для разделов, не используй слово 'Нур-султан', не используй иконки, не используй переносы строк на новую строку, не используй пункты, не используй жирный шрифт. Текст должен быть полностью слитным")
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/goods/index")
async def generate_meta_description(request_body: Txt):
    try:
        meta_res = generate_text(f"Напиши уникальное индексируемое в google мета-описание не более 200 слов для товара, продаваемого на международном маркете Mytrade.kz на основе этого текста: {request_body.text}")
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/goods/seo")
async def generate_meta_description(request_body: Txt):
    try:
        meta_res = generate_text(f"Напиши уникальный seo-текст не более 500 слов о возможности найти на международном маркете Mytrade товар «{request_body.text}» продаваемый магазинами со всего мира, включая Казахстан. Приведи примеры применения товара «{request_body.text}». Перечисли кратко несколько городов мира, в которых магазины продают этот товар в маркете Mytrade.kz. В тексте не используй заголовки для разделов, не используй слово 'Нур-султан', не используй иконки, не используй переносы строк на новую строку, не используй пункты, не используй жирный шрифт. Текст должен быть полностью слитным.")
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/category/seo")
async def generate_meta_description(request_body: Txt):
    try:
        meta_res = generate_text(f"Напиши уникальный seo-текст из 500 слов о продаже товаров из категории «{request_body.text}» на международном маркете Mytrade.kz. Расскажи о широком ассортименте товаров в категории «{request_body.text}» от продавцов и производителей со всего мира. Перечисли продаваемые в маркете Mytrade.kz товары из категории «{request_body.text}» и приведи примеры их применения. Перечисли кратко несколько городов мира, в которых магазины продают товары из данной категории на маркете Mytrade.kz. В тексте не используй заголовки для разделов, не используй слово 'Нур-султан', не используй иконки, не используй переносы строк на новую строку, не используй пункты, не используй жирный шрифт. Текст должен быть полностью слитным")
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/category/index")
async def generate_meta_description(request_body: Txt):
    try:
        meta_res = generate_text(f"Напиши уникальное индексируемое в google мета-описание не более 200 слов для категории международного маркета Mytrade.kz «{request_body.text}». Напиши кратко какие товары можно купить в данной категории.")
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/vacancy/index")
async def generate_meta_description(request_body: Txt):
    try:
        meta_res = generate_text(f"Напиши уникальное индексируемое в google мета-описание не более 200 слов для вакансии компании, опубликованным на международном маркете Mytrade.kz на основе этого текста: «{request_body.text}».")
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/vacancy/seo")
async def generate_meta_description(request_body: Txt):
    try:
        meta_res = generate_text(f"Напиши уникальный seo-текст не более 500 слов о возможности найти на международном сервисе поиска работы Mytrade.kz вакансии «{request_body.text}» в различных странах мира, включая Казахстан. Приведи примеры вакансий «{request_body.text}». Перечисли кратко несколько городов мира, в которых компании ищут кандидатов на данную вакансию в сервисе поиска работы Mytrade.kz. В тексте не используй заголовки для разделов, не используй слово 'Нур-султан', не используй иконки, не используй переносы строк на новую строку, не используй пункты, не используй жирный шрифт. Текст должен быть полностью слитным.")
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/vacancy/resume/index")
async def generate_meta_description(request_body: Txt):
    try:
        meta_res = generate_text(f" «Напиши уникальное индексируемое в google мета-описание не более 200 слов для резюме соискателя работы, опубликованным на международном маркете Mytrade.kz на основе этого текста: «{request_body.text}».")
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/vacancy/resume/seo")
async def generate_meta_description(request_body: Txt):
    try:
        meta_res = generate_text(f"Напиши уникальный seo-текст не более 500 слов о возможности найти на международном сервисе поиска работы Mytrade.kz резюме кандидатов и соискателей на должность «{request_body.text}» в различных странах мира, включая Казахстан. Приведи примеры резюме «{request_body.text}». Перечисли кратко несколько городов мира, в которых соискатели ищут работу на должность (вставить полученное от БЭК МТ наименование желаемой должности) в сервисе поиска работы Mytrade.kz. В тексте не используй заголовки для разделов, не используй слово 'Нур-султан', не используй иконки, не используй переносы строк на новую строку, не используй пункты, не используй жирный шрифт. Текст должен быть полностью слитным.")
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/phys/seo")
async def generate_meta_description(request_body: Txt):
    try:
        meta_res = generate_text(f"Напиши уникальный seo-текст не более 500 слов о возможности на международной платформе Mytrade.kz смотреть объявления о продаваемых товарах, услугах, недвижимости, автомобилей, мотоциклов, скутеров, спецтехники от частных физических лиц на их личных странницах. А также возможности смотреть об объявленных закупках различных товаров и услуг частными лицами, которые они размещают в своих профилях. Напиши также, что на странницах частных лиц можно добавить в избранные понравившиеся объявления и отправить автору объявления сообщения на удобном языке отправителя. В тексте не используй заголовки для разделов, не используй слово 'Нур-султан', не используй иконки, не используй переносы строк на новую строку, не используй пункты, не используй жирный шрифт. Текст должен быть полностью слитным: {request_body.text}")
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/phys/index")
async def generate_meta_description(request_body: Txt):
    try:
        meta_res = generate_text(f"Напиши уникальный индексируемый в google мета-текст не более 200 слов для текста «{request_body.text}». При генерации ответа не используй ID пользователя.")
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/jud/seo")
async def generate_meta_description(request_body: Txt):
    try:
        meta_res = generate_text(f"Напиши уникальный seo-текст не более 500 слов о возможности найти на международной торговой платформе Mytrade различные товары и услуги от магазинов и компаний со всего мира, включая Казахстан. Приведи примеры продаваемых товаров и услуг от компаний из отрасли «{request_body.text}». Перечисли кратко несколько городов мира, в которых компании продают товары и услуги в маркете и доске объявлений Mytrade.kz. В тексте не используй заголовки для разделов, не используй слово 'Нур-султан', не используй иконки, не используй переносы строк на новую строку, не используй пункты, не используй жирный шрифт. Текст должен быть полностью слитным. ")
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/jud/index")
async def generate_meta_description(request_body: Txt):
    try:
        meta_res = generate_text(f"Напиши уникальный индексируемый в google мета-текст не более 200 слов для текста: «{request_body.text}».")
        return JSONResponse(content={"meta": meta_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8020)
