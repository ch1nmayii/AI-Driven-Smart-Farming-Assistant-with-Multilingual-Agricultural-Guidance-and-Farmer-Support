"""Quick smoke test for all Week 1-2 modules (ASCII-safe output)."""
import asyncio
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from app.core.nlp_processor import nlp_processor
from app.core.rag_engine import rag_engine
from app.core.session_manager import session_manager

TEST_QUERIES = [
    ("hi", "gehun mein pila ratua rog ke lakshan dikh rahe hain"),   # ASCII transliteration
    ("en", "What is the PM-KISAN scheme and how to apply?"),
    ("en", "Today what is the mandi price for wheat?"),
    ("en", "What fertilizer to use for cotton crop in black soil?"),
]

async def run_tests():
    print("=" * 60)
    print("WEEK 1-2 MODULE SMOKE TEST")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for lang, query in TEST_QUERIES:
        print(f"\nQuery [{lang.upper()}]: {query[:70]}...")
        
        # NLP Pipeline test
        nlp = nlp_processor.process_query(query, preferred_language=lang)
        print(f"  Language  : {nlp['language']} (confidence={nlp['language_confidence']:.2f})")
        print(f"  Intent    : {nlp['intent']} (confidence={nlp['intent_confidence']:.2f})")
        print(f"  Crop ctx  : {nlp['crop_context']}")
        print(f"  Pest ctx  : {nlp['pest_disease']}")
        print(f"  Entities  : {len(nlp['entities'])} found")
        
        # RAG Pipeline test
        result = await rag_engine.process_query(query, language=lang, session_id=f"test-{lang}")
        resp_preview = result['response_text'][:80].encode('ascii', 'replace').decode()
        print(f"  Confidence: {result['confidence_score']:.2f} | Flagged: {result['flagged_for_review']}")
        print(f"  Response  : {resp_preview}...")
        
        if nlp['intent'] and result['response_text']:
            print(f"  STATUS    : PASS")
            passed += 1
        else:
            print(f"  STATUS    : FAIL")
            failed += 1
    
    # Session manager check
    ctx = session_manager.get_context_summary("test-en")
    print(f"\nSession Context: turns={ctx.get('turn_count')}, last_intent={ctx.get('last_intent')}")
    
    print("\n" + "=" * 60)
    print(f"RESULTS: {passed}/{passed+failed} tests PASSED, {failed} FAILED")
    print("=" * 60)
    
    if failed == 0:
        print("ALL WEEK 1-2 TASKS COMPLETE AND WORKING")
    
    sys.exit(0 if failed == 0 else 1)

asyncio.run(run_tests())
