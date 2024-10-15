import ctranslate2
import transformers
# from lang_list import lang_list
from lang_list import langs
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import re


def clean_html_tags(text):
    clean_text = re.sub(r'<[^>]+>', '', text)
    return clean_text


class translator:
    def __init__(self):
        self.lang_list = langs
        self.model = AutoModelForSeq2SeqLM.from_pretrained('./my_model')
        self.tokenizer = AutoTokenizer.from_pretrained('./my_model')
        self.translation_pipeline = pipeline(
            'translation',
            model=self.model,
            tokenizer=self.tokenizer,
            max_length=4000
        )

    def translate(self, src_lang, tgt_lang, input_text):
        output = self.translation_pipeline(input_text, src_lang=src_lang, tgt_lang=tgt_lang)
        return output[0]['translation_text'] if output else ""
