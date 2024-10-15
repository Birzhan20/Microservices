import ctranslate2
import transformers
# from lang_list import lang_list
from lang_list import lang_list
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import re


def clean_html_tags(text):
    clean_text = re.sub(r'<[^>]+>', '', text)
    return clean_text


class translator:
    def __init__(self):
        self.lang_list = lang_list

    def translate(self, src_lang, tgt_lang, input_text):

        input_text = clean_html_tags(input_text)
        checkpoint = 'facebook/nllb-200-distilled-1.3B'

        model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint)
        tokenizer = AutoTokenizer.from_pretrained(checkpoint)

        translation_pipeline = pipeline('translation',
                                        model=model,
                                        tokenizer=tokenizer,
                                        src_lang=src_lang,
                                        tgt_lang=tgt_lang,
                                        max_length=4000)

        output = translation_pipeline(input_text, src_lang=src_lang, tgt_lang=tgt_lang)
        return output[0]['translation_text'] if output else ""

        # output = translation_pipeline(input_text)
        # return output[0]['translation_text'] if output else ""



