import json
import os
from typing import List, Dict, Any, Optional
from app.config import settings

class KnowledgeBase:
    def __init__(self):
        self.kb_file = os.path.join(settings.DATA_DIR, "agricultural_kb.json")
        self.entries: List[Dict[str, Any]] = []
        self.load()

    def load(self):
        if os.path.exists(self.kb_file):
            try:
                with open(self.kb_file, "r", encoding="utf-8") as f:
                    self.entries = json.load(f)
            except Exception as e:
                print(f"Error loading knowledge base: {e}")
                self.entries = []
        else:
            self.entries = []

    def save(self):
        os.makedirs(settings.DATA_DIR, exist_ok=True)
        with open(self.kb_file, "w", encoding="utf-8") as f:
            json.dump(self.entries, f, ensure_ascii=False, indent=2)

    def search(self, query: str, language: str = "hi") -> List[Dict[str, Any]]:
        query_lower = query.lower()
        results = []
        for entry in self.entries:
            score = 0
            # Keyword matching
            for kw in entry.get("keywords", []):
                if kw.lower() in query_lower:
                    score += 3
            # Title & content matching
            title = entry.get("title", "").lower()
            if query_lower in title:
                score += 2
            
            content_key = f"content_{language}" if f"content_{language}" in entry else "content_en"
            content = entry.get(content_key, "").lower()
            if any(word in content for word in query_lower.split() if len(word) > 2):
                score += 1
            
            if score > 0:
                results.append((score, entry))
        
        # Sort descending by score
        results.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in results]

    def add_entry(self, entry: Dict[str, Any]):
        self.entries.append(entry)
        self.save()

    def get_all(self) -> List[Dict[str, Any]]:
        return self.entries

kb_instance = KnowledgeBase()
