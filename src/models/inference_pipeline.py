import torch
from transformers import pipeline
from .model_loader import get_model_loader
import logging

logger = logging.getLogger(__name__)


class InferencePipeline:
    _instance = None
    _pipeline = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(InferencePipeline, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """
        Modeli ve tokenizer'ı yükleyip text-generation pipeline'ını kurar.
        Bu işlem sadece ilk çağrıldığında bir kez yapılır (Singleton).
        """
        if self._pipeline is not None:
            logger.info("Inference pipeline zaten mevcut.")
            return

        try:
            logger.info("🤖 Inference pipeline başlatılıyor... Model yükleniyor...")
            model_loader = get_model_loader()

            # Mevcut gelişmiş loader'ınızı kullanarak modeli yükleyin
            # Model adını varsayılan olarak ayarlıyoruz, ileride değiştirilebilir.
            model, tokenizer = model_loader.load_base_model(
                model_name="bigcode/starcoder2-3b",
                use_quantization=True,
                use_cache=True
            )

            if model is None or tokenizer is None:
                raise RuntimeError("Model veya tokenizer yüklenemedi.")

            self._pipeline = pipeline(
                "text-generation",
                model=model,
                tokenizer=tokenizer,
                device_map="auto",
                max_new_tokens=1024,
                repetition_penalty=1.1
            )
            logger.info("✅ Inference pipeline başarıyla kuruldu.")
        except Exception as e:
            logger.error(f"❌ Inference pipeline kurulumunda kritik hata: {e}", exc_info=True)
            self._pipeline = None

    def generate(self, prompt: str) -> str:
        """
        Verilen prompt'a göre yapay zekadan bir cevap üretir.
        """
        if self._pipeline is None:
            logger.error("❌ Pipeline kurulu değil. Cevap üretilemiyor.")
            return "Yapay zeka modeli şu anda kullanılamıyor. Lütfen logları kontrol edin."

        try:
            logger.info("🧠 Yapay zekadan cevap üretiliyor...")

            # StarCoder2 için önerilen prompt formatı
            formatted_prompt = f"<|user|>\n{prompt}<|end|>\n<|assistant|>"

            sequences = self._pipeline(
                formatted_prompt,
                do_sample=True,
                top_k=10,
                num_return_sequences=1,
                eos_token_id=self._pipeline.tokenizer.eos_token_id,
            )

            generated_text = sequences[0]['generated_text']

            # Prompt'u temizleyip sadece asistanın cevabını al
            assistant_response = generated_text.split("<|assistant|>")[-1].strip()

            logger.info("✅ Cevap başarıyla üretildi.")
            return assistant_response

        except Exception as e:
            logger.error(f"❌ Cevap üretimi sırasında hata: {e}", exc_info=True)
            return f"Cevap üretilirken bir hata oluştu: {str(e)}"


# Global erişim için bir fonksiyon
def get_inference_pipeline() -> InferencePipeline:
    return InferencePipeline()