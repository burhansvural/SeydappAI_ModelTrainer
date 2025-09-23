# src/research/knowledge_extractor.py
"""
Knowledge Extractor
Extracts structured knowledge from text content
"""

import re
import logging
from typing import List, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class KnowledgeExtractor:
    """Extract structured knowledge from text content"""
    
    def __init__(self):
        self.code_patterns = {
            'python_function': r'def\s+(\w+)\s*\([^)]*\):',
            'python_class': r'class\s+(\w+)(?:\([^)]*\))?:',
            'python_import': r'(?:from\s+\w+\s+)?import\s+(\w+)',
            'javascript_function': r'function\s+(\w+)\s*\([^)]*\)',
            'variable_assignment': r'(\w+)\s*=\s*[^=]'
        }
        logger.info("🧠 KnowledgeExtractor initialized")
    
    def extract_knowledge(self, text_content: str) -> Dict[str, Any]:
        """
        Extract knowledge from text content
        
        Args:
            text_content: Text to extract knowledge from
            
        Returns:
            Dictionary containing extracted knowledge
        """
        try:
            knowledge = {
                'concepts': self._extract_concepts(text_content),
                'code_examples': self._extract_code_examples(text_content),
                'definitions': self._extract_definitions(text_content),
                'keywords': self._extract_keywords(text_content),
                'metadata': {
                    'extraction_time': datetime.now(),
                    'content_length': len(text_content),
                    'word_count': len(text_content.split())
                }
            }
            
            logger.info(f"✅ Extracted knowledge: {len(knowledge['concepts'])} concepts, {len(knowledge['code_examples'])} code examples")
            return knowledge
            
        except Exception as e:
            logger.error(f"❌ Knowledge extraction error: {e}")
            return {}
    
    def extract_code_examples(self, content: str) -> List[Dict]:
        """Extract code examples from content"""
        try:
            code_examples = []
            
            # Extract code blocks
            code_blocks = re.findall(r'```(?:\w+)?\n(.*?)\n```', content, re.DOTALL)
            for i, code in enumerate(code_blocks):
                code_examples.append({
                    'type': 'code_block',
                    'content': code.strip(),
                    'language': self._detect_language(code),
                    'index': i
                })
            
            # Extract inline code
            inline_code = re.findall(r'`([^`]+)`', content)
            for i, code in enumerate(inline_code):
                if len(code) > 10:  # Only longer inline code
                    code_examples.append({
                        'type': 'inline_code',
                        'content': code.strip(),
                        'language': self._detect_language(code),
                        'index': i
                    })
            
            logger.info(f"✅ Extracted {len(code_examples)} code examples")
            return code_examples
            
        except Exception as e:
            logger.error(f"❌ Code extraction error: {e}")
            return []
    
    def create_concept_map(self, knowledge: Dict) -> Dict:
        """Create a concept map from extracted knowledge"""
        try:
            concept_map = {
                'nodes': [],
                'relationships': [],
                'metadata': {
                    'creation_time': datetime.now(),
                    'total_concepts': 0
                }
            }
            
            # Create nodes from concepts
            concepts = knowledge.get('concepts', [])
            for i, concept in enumerate(concepts):
                concept_map['nodes'].append({
                    'id': i,
                    'label': concept,
                    'type': 'concept',
                    'weight': 1.0
                })
            
            # Create relationships (simplified)
            for i in range(len(concepts) - 1):
                concept_map['relationships'].append({
                    'source': i,
                    'target': i + 1,
                    'type': 'related_to',
                    'weight': 0.5
                })
            
            concept_map['metadata']['total_concepts'] = len(concepts)
            
            logger.info(f"✅ Created concept map with {len(concepts)} nodes")
            return concept_map
            
        except Exception as e:
            logger.error(f"❌ Concept map creation error: {e}")
            return {}
    
    def _extract_concepts(self, text: str) -> List[str]:
        """Extract key concepts from text"""
        # Simple concept extraction based on capitalized words and technical terms
        concepts = []
        
        # Technical terms
        tech_terms = re.findall(r'\b[A-Z][a-z]*(?:[A-Z][a-z]*)*\b', text)
        concepts.extend(tech_terms)
        
        # Programming concepts
        prog_concepts = re.findall(r'\b(?:function|class|method|variable|array|object|string|integer|boolean)\b', text, re.IGNORECASE)
        concepts.extend(prog_concepts)
        
        # Remove duplicates and return
        return list(set(concepts))
    
    def _extract_code_examples(self, text: str) -> List[str]:
        """Extract code examples from text"""
        code_examples = []
        
        # Code blocks
        code_blocks = re.findall(r'```(?:\w+)?\n(.*?)\n```', text, re.DOTALL)
        code_examples.extend([code.strip() for code in code_blocks])
        
        # Function definitions
        functions = re.findall(r'def\s+\w+\s*\([^)]*\):[^}]+', text)
        code_examples.extend(functions)
        
        return code_examples
    
    def _extract_definitions(self, text: str) -> List[Dict]:
        """Extract definitions from text"""
        definitions = []
        
        # Pattern: "X is Y" or "X: Y"
        definition_patterns = [
            r'(\w+(?:\s+\w+)*)\s+is\s+([^.]+)',
            r'(\w+(?:\s+\w+)*)\s*:\s*([^.]+)'
        ]
        
        for pattern in definition_patterns:
            matches = re.findall(pattern, text)
            for term, definition in matches:
                definitions.append({
                    'term': term.strip(),
                    'definition': definition.strip()
                })
        
        return definitions
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text"""
        # Simple keyword extraction
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Filter common words
        common_words = {'the', 'is', 'at', 'which', 'on', 'and', 'a', 'to', 'are', 'as', 'was', 'with', 'for'}
        keywords = [word for word in words if len(word) > 3 and word not in common_words]
        
        # Count frequency and return top keywords
        from collections import Counter
        word_counts = Counter(keywords)
        return [word for word, count in word_counts.most_common(20)]
    
    def _detect_language(self, code: str) -> str:
        """Detect programming language of code snippet"""
        if 'def ' in code or 'import ' in code or 'print(' in code:
            return 'python'
        elif 'function' in code or 'var ' in code or 'let ' in code:
            return 'javascript'
        elif '#include' in code or 'int main' in code:
            return 'c'
        elif 'public class' in code or 'System.out' in code:
            return 'java'
        else:
            return 'unknown'


if __name__ == "__main__":
    # Test the extractor
    extractor = KnowledgeExtractor()
    
    sample_text = """
    Python is a high-level programming language. 
    
    ```python
    def hello_world():
        print("Hello, World!")
        return True
    ```
    
    A function is a block of code that performs a specific task.
    """
    
    knowledge = extractor.extract_knowledge(sample_text)
    print(f"Extracted knowledge: {knowledge}")