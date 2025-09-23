# Search results [4] SambaLingo Turkish pattern
import json
import logging
from transformers import AutoTokenizer
from typing import List, Dict, Any, Optional


class TurkishCodingPreprocessor:
    """Turkish coding conversation preprocessor - Search results [4] pattern"""

    def __init__(self, model_name: str = "bigcode/starcoder2-3b"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        self.logger = logging.getLogger(__name__)
        self.max_length = 512  # RTX 3060 optimal

    def preprocess_jsonl_dataset(self, input_path: str, output_path: str) -> Dict[str, Any]:
        """Preprocess JSONL dataset for training"""

        processed_examples = []
        stats = {'total': 0, 'processed': 0, 'skipped': 0, 'errors': []}

        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    try:
                        data = json.loads(line.strip())
                        stats['total'] += 1

                        # Process conversation format
                        processed = self._process_conversation(data, line_num, stats)
                        if processed:
                            processed_examples.append(processed)
                            stats['processed'] += 1
                        else:
                            stats['skipped'] += 1

                    except Exception as e:
                        stats['errors'].append(f"Line {line_num}: {str(e)}")
                        stats['skipped'] += 1

            # Save processed dataset
            if processed_examples:
                self._save_processed_dataset(processed_examples, output_path)
                self.logger.info(f"✅ Processed {stats['processed']}/{stats['total']} examples")

            return stats

        except Exception as e:
            self.logger.error(f"Preprocessing error: {e}")
            return {'error': str(e)}

    def _process_conversation(self, data: Dict, line_num: int, stats: Dict) -> Optional[Dict]:
        """Process single conversation - Turkish coding format"""

        try:
            # Format conversation for causal LM
            instruction = data['instruction'].strip()
            user_input = data.get('input', '').strip()
            output = data['output'].strip()

            # Create conversation format
            if user_input:
                conversation_text = f"Kullanıcı: {instruction}\nGirdi: {user_input}\nAsistan: {output}"
            else:
                conversation_text = f"Kullanıcı: {instruction}\nAsistan: {output}"

            # Tokenize and check length
            tokens = self.tokenizer.encode(conversation_text)
            if len(tokens) > self.max_length:
                # Truncate if too long
                conversation_text = self.tokenizer.decode(
                    tokens[:self.max_length - 1],
                    skip_special_tokens=True
                )
                self.logger.warning(f"Line {line_num}: Truncated long conversation")

            return {
                'text': conversation_text,
                'length': len(tokens),
                'source': 'turkish_coding_conversation'
            }

        except Exception as e:
            stats['errors'].append(f"Line {line_num}: Processing error - {str(e)}")
            return None

    def _save_processed_dataset(self, examples: List[Dict], output_path: str):
        """Save processed dataset"""
        with open(output_path, 'w', encoding='utf-8') as f:
            for example in examples:
                f.write(json.dumps(example, ensure_ascii=False) + '\n')
