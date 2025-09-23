# Önerilen içerik - Search results [1] pattern
import json
import logging
from typing import List, Dict, Any
import re


class TurkishCodingDataValidator:
    """Turkish coding conversation validator - Search results [1] ETL pattern"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.min_instruction_length = 10
        self.min_output_length = 50
        self.required_fields = ['instruction', 'input', 'output']

    def validate_jsonl_file(self, file_path: str) -> Dict[str, Any]:
        """Validate JSONL dataset quality"""
        stats = {
            'total_examples': 0,
            'valid_examples': 0,
            'errors': [],
            'quality_metrics': {}
        }

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    try:
                        data = json.loads(line.strip())
                        stats['total_examples'] += 1

                        # Validate structure
                        if self._validate_structure(data, line_num, stats):
                            # Validate content quality
                            if self._validate_content_quality(data, line_num, stats):
                                stats['valid_examples'] += 1

                    except json.JSONDecodeError as e:
                        stats['errors'].append(f"Line {line_num}: JSON decode error - {e}")

            # Calculate quality metrics
            stats['quality_metrics'] = self._calculate_quality_metrics(stats)
            return stats

        except Exception as e:
            self.logger.error(f"File validation error: {e}")
            return {'error': str(e)}

    def _validate_structure(self, data: Dict, line_num: int, stats: Dict) -> bool:
        """Validate data structure"""
        missing_fields = [field for field in self.required_fields if field not in data]
        if missing_fields:
            stats['errors'].append(f"Line {line_num}: Missing fields - {missing_fields}")
            return False
        return True

    def _validate_content_quality(self, data: Dict, line_num: int, stats: Dict) -> bool:
        """Validate content quality - Turkish coding focus"""

        # Check instruction length
        if len(data['instruction']) < self.min_instruction_length:
            stats['errors'].append(f"Line {line_num}: Instruction too short")
            return False

        # Check output length and code presence
        output = data['output']
        if len(output) < self.min_output_length:
            stats['errors'].append(f"Line {line_num}: Output too short")
            return False

        # Check for code blocks in coding conversations
        if 'python' in data['instruction'].lower() or 'kod' in data['instruction'].lower():
            if '```' not in output:
                stats['errors'].append(f"Line {line_num}: Coding question missing code block")
                return False

        # Turkish language check (basic)
        turkish_chars = re.search(r'[çğıöşüÇĞIÖŞÜ]', data['instruction'])
        if not turkish_chars:
            stats['errors'].append(f"Line {line_num}: Instruction may not be Turkish")
            return False

        return True

    def _calculate_quality_metrics(self, stats: Dict) -> Dict[str, Any]:
        """Calculate dataset quality metrics"""
        total = stats['total_examples']
        valid = stats['valid_examples']

        return {
            'validity_rate': (valid / total * 100) if total > 0 else 0,
            'error_rate': (len(stats['errors']) / total * 100) if total > 0 else 0,
            'recommended_action': self._get_recommendation(valid, total)
        }

    def _get_recommendation(self, valid: int, total: int) -> str:
        """Get recommendation based on quality"""
        if total == 0:
            return "No data found"

        validity_rate = valid / total * 100

        if validity_rate >= 90:
            return "Dataset ready for training"
        elif validity_rate >= 70:
            return "Good quality - minor fixes needed"
        elif validity_rate >= 50:
            return "Medium quality - significant improvements needed"
        else:
            return "Poor quality - major rework required"
