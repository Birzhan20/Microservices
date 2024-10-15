from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

checkpoint = 'facebook/nllb-200-distilled-1.3B'

model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint)
model.save_pretrained('./my_model')

tokenizer = AutoTokenizer.from_pretrained(checkpoint)
tokenizer.save_pretrained('./my_model')

