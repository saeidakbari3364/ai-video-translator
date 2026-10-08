from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


class Translator:
    def __init__(
        self,
        model_name: str = "facebook/nllb-200-distilled-600M",
    ):
        print("Loading translation model...")

        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name
        )

        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            model_name
        )

        # English
        self.source_language = "eng_Latn"

        # Persian
        self.target_language = "pes_Arab"

        self.tokenizer.src_lang = self.source_language

    def translate(self, text: str) -> str:

        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            padding=True,
            truncation=True,
        )

        translated_tokens = self.model.generate(
            **inputs,
            forced_bos_token_id=self.tokenizer.convert_tokens_to_ids(
                self.target_language
            ),
            max_length=512,
        )

        translated_text = self.tokenizer.batch_decode(
            translated_tokens,
            skip_special_tokens=True,
        )[0]

        return translated_text.strip()

    def translate_segments(self, segments):

        translated_segments = []

        for segment in segments:

            translated_text = self.translate(
                segment["text"]
            )

            translated_segments.append(
                {
                    "start": segment["start"],
                    "end": segment["end"],
                    "text": translated_text,
                }
            )

        return translated_segments