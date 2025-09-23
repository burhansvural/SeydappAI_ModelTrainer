# src/knowledge/knowledge_processor.py

import logging
from typing import List, Dict, Optional  # ✅ CRITICAL: Typing imports eklendi
import json
import re
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

class KnowledgeProcessor:
    """✅ SEARCH RESULTS [2] PATTERN: ETL pipeline for knowledge graph[2]"""

    def __init__(self):
        self.knowledge_graph_file = Path("storage/data/knowledge_graph.json")
        self.knowledge_graph_file.parent.mkdir(parents=True, exist_ok=True)

        # ✅ Load existing knowledge graph
        self.knowledge_graph = self.load_knowledge_graph()
        self.entity_cache = {}

        logger.info(f"🧠 Knowledge Processor initialized - {len(self.knowledge_graph)} entities loaded")

    def load_knowledge_graph(self) -> Dict:
        """✅ SEARCH RESULTS [1] PATTERN: Load existing data[1]"""
        try:
            if self.knowledge_graph_file.exists():
                with open(self.knowledge_graph_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    logger.info(f"📂 Loaded {len(data)} entities from knowledge graph")
                    return data
            else:
                logger.info("📂 Creating new knowledge graph")
                return {}
        except Exception as e:
            logger.warning(f"⚠️ Knowledge graph load error: {e}")
            return {}

    def save_knowledge_graph(self):
        """✅ SEARCH RESULTS [1] PATTERN: Save data to file[1]"""
        try:
            with open(self.knowledge_graph_file, 'w', encoding='utf-8') as f:
                json.dump(self.knowledge_graph, f, ensure_ascii=False, indent=2)

            logger.info(f"💾 Knowledge graph saved: {len(self.knowledge_graph)} entities")

        except Exception as e:
            logger.error(f"❌ Knowledge graph save error: {e}")


    def extract_entities(self, item: Dict) -> List[str]:
        """Extract key programming entities from text"""
        try:
            text = f"{item.get('question', '')} {item.get('answer', '')}"

            # Simple entity extraction patterns
            entities = []

            # Programming languages
            languages = re.findall(r'\b(python|javascript|java|c\+\+|rust|go)\b', text, re.IGNORECASE)
            entities.extend([f"LANG:{lang.lower()}" for lang in languages])

            # Libraries/Frameworks
            frameworks = re.findall(r'\b(django|flask|fastapi|pandas|numpy|pytorch|tensorflow)\b', text, re.IGNORECASE)
            entities.extend([f"FRAMEWORK:{fw.lower()}" for fw in frameworks])

            # Concepts
            concepts = re.findall(r'\b(machine learning|neural network|api|database|async|training)\b', text,
                                  re.IGNORECASE)
            entities.extend([f"CONCEPT:{concept.lower()}" for concept in concepts])

            return entities

        except Exception as e:
            logger.warning(f"⚠️ Entity extraction error: {e}")
            return []

    def transform_to_graph(self, entities: List[str], item: Dict) -> List[Dict]:
        """Transform entities to graph nodes"""
        try:
            graph_nodes = []

            for entity in entities:
                node = {
                    "id": entity,
                    "type": entity.split(":"),
                    "name": entity.split(":")[1],
                    "source_question": item.get("question", ""),
                    "source_answer": item.get("answer", ""),
                    "confidence": item.get("confidence", 0.0),
                    "timestamp": datetime.now().isoformat()
                }
                graph_nodes.append(node)

            return graph_nodes

        except Exception as e:
            logger.warning(f"⚠️ Graph transformation error: {e}")
            return []

    def load_to_graph(self, graph_nodes: List[Dict]):
        """Load nodes to knowledge graph + AUTO SAVE"""
        try:
            for node in graph_nodes:
                node_id = node["id"]
                if node_id not in self.knowledge_graph:
                    self.knowledge_graph[node_id] = {
                        "occurrences": 0,
                        "connections": [],
                        "metadata": {}
                    }

                # Increment occurrences
                self.knowledge_graph[node_id]["occurrences"] += 1
                self.knowledge_graph[node_id]["metadata"] = {
                    "type": node["type"],
                    "name": node["name"],
                    "last_updated": node["timestamp"],
                    "confidence": node["confidence"]
                }

            # ✅ SEARCH RESULTS [1] CRITICAL: Auto-save after updates[1]
            self.save_knowledge_graph()

        except Exception as e:
            logger.warning(f"⚠️ Graph loading error: {e}")

    async def process_research_data(self, knowledge_items: List[Dict]) -> Dict:
        """Search results [1] ETL: Extract, Transform, Load[1]"""
        try:
            processed_nodes = 0

            for item in knowledge_items:
                # ✅ Extract key entities
                entities = self.extract_entities(item)

                # ✅ Transform to graph structure
                graph_nodes = self.transform_to_graph(entities, item)

                # ✅ Load to knowledge graph
                self.load_to_graph(graph_nodes)

                processed_nodes += len(graph_nodes)

            logger.info(f"✅ Processed {processed_nodes} knowledge nodes")

            return {
                "processed_nodes": processed_nodes,
                "graph_size": len(self.knowledge_graph),
                "unique_entities": len(self.knowledge_graph),
                "status": "completed"
            }

        except Exception as e:
            logger.error(f"❌ Knowledge processing error: {e}")
            return {"processed_nodes": 0, "graph_size": 0, "status": "error"}

    def get_knowledge_summary(self) -> Dict:
        """Get knowledge graph summary for UI display"""
        return {
            "total_entities": len(self.knowledge_graph),
            "top_concepts": self._get_top_concepts(5),
            "last_updated": datetime.now().strftime("%H:%M")
        }

    def _get_top_concepts(self, limit: int) -> List[str]:
        """Get most frequent concepts"""
        try:
            sorted_entities = sorted(
                self.knowledge_graph.items(),
                key=lambda x: x[1]["occurrences"],
                reverse=True
            )
            return [entity for entity in sorted_entities[:limit]]
        except:
            return []
