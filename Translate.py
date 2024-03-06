from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM


def translate(model, text):
  translator = pipeline('translation', model=model['model'], tokenizer=model['tokenizer'],
                        src_lang=model['source_lang'], tgt_lang=model['target_lang'])

  output = translator(text)

  return output[0]['translation_text']


def text_HUN_to_text_ENG(text_hun: str) -> str:
    models = [
        {
            'model_name': 'facebook/nllb-200-distilled-600M',
            'source_lang': 'hun_Latn',
            'target_lang': 'eng_Latn',
        },
        {
            'model_name': 'Helsinki-NLP/opus-mt-hu-en',
            'source_lang': 'hun_Latn',
            'target_lang': 'eng_Latn',
        },
        {
            'model_name': 'facebook/m2m100_418M',
            'source_lang': 'hu',
            'target_lang': 'en',
        }
    ]

    # Downloading translator model
    name = models[1]['model_name']
    models[1]['model'] = AutoModelForSeq2SeqLM.from_pretrained(name)
    models[1]['tokenizer'] = AutoTokenizer.from_pretrained(name)


    translation_text = translate(models[1],text_hun)
    return translation_text
