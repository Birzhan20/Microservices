from transformers import AutoTokenizer, AutoModelForCausalLM

model_name = "ai-forever/rugpt3small_based_on_gpt2"
save_directory = "./ai"

print("Загрузка модели и токенайзера...")
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

print(f"Сохранение модели и токенайзера в директорию '{save_directory}'...")
tokenizer.save_pretrained(save_directory)
model.save_pretrained(save_directory)

print("Загрузка завершена!")
