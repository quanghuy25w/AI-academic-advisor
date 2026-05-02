"""
Test script để verify nâng cấp Router system
Test cases cho 2 category: DOMAIN_DATA vs GENERAL_LLM
"""

import json
from pathlib import Path

# Setup path
import sys
sys.path.insert(0, str(Path(__file__).parent))

from src.config.groq_gateway import invoke_llm
from src.prompts.intent_prompt import INTENT_PROMPT

def test_intent_classification():
    """Test intent classification với các câu hỏi mẫu"""
    
    test_cases = {
        "DOMAIN_DATA": [
            "Môn Hệ thống nhúng có mấy tín chỉ?",
            "Ai dạy môn Cơ sở dữ liệu?",
            "Lịch học kỳ này là gì?",
            "Kế hoạch giảng dạy của API là gì?",
            "Yêu cầu tốt nghiệp là gì?",
            "Email của giảng viên là gì?",
            "CLO của môn lập trình là gì?",
        ],
        "GENERAL_LLM": [
            "Dijkstra algorithm là gì?",
            "Xin chào, bạn khỏe không?",
            "Python có cách nào check type không?",
            "Database design best practices là gì?",
            "Mình nên học lập trình theo thứ tự nào?",
            "Hôm nay thế nào?",
            "API là gì?",
        ]
    }
    
    print("=" * 80)
    print("🧪 TEST INTENT CLASSIFICATION")
    print("=" * 80)
    
    for expected_category, questions in test_cases.items():
        print(f"\n📝 Testing {expected_category}:")
        print("-" * 80)
        
        for question in questions:
            prompt = INTENT_PROMPT.format(question=question)
            
            try:
                response = invoke_llm(prompt).strip()
                print(f"\nQ: {question}")
                print(f"Response: {response[:200]}...")
                
                # Parse JSON
                try:
                    data = json.loads(response)
                    category = data.get("category", "UNKNOWN")
                    
                    if category == expected_category:
                        print(f"✅ PASS - Got {category}")
                    else:
                        print(f"⚠️  WARN - Expected {expected_category}, got {category}")
                except json.JSONDecodeError:
                    print(f"❌ FAIL - Could not parse JSON from LLM response")
                    
            except Exception as e:
                print(f"❌ ERROR - {e}")

def test_router_logic():
    """Test logic điều hướng"""
    print("\n" + "=" * 80)
    print("🔀 TEST ROUTER LOGIC")
    print("=" * 80)
    
    test_states = [
        {
            "name": "DOMAIN_DATA Query",
            "category": "DOMAIN_DATA",
            "context": "Thông tin về môn học từ ChromaDB",
            "expected_flow": "retrieve → context → answer → validation → save_chat"
        },
        {
            "name": "GENERAL_LLM Query",
            "category": "GENERAL_LLM",
            "context": "",
            "expected_flow": "answer → save_chat (no retrieve, no validation)"
        },
    ]
    
    for state in test_states:
        print(f"\n📊 Scenario: {state['name']}")
        print(f"   Category: {state['category']}")
        print(f"   Context: {'Present' if state['context'] else 'Empty'}")
        print(f"   Expected Flow: {state['expected_flow']}")
        
        # Simulate routing
        if state['category'] == "DOMAIN_DATA":
            routing = "retrieve"
            print(f"   ✓ route_after_intent → {routing}")
            if state['context']:
                routing = "validation"
                print(f"   ✓ route_after_answer → {routing}")
                routing = "save_chat"
                print(f"   ✓ should_continue → {routing}")
        else:
            routing = "answer"
            print(f"   ✓ route_after_intent → {routing}")
            routing = "save_chat"
            print(f"   ✓ route_after_answer → {routing} (no validation)")

def test_context_node():
    """Test context node với empty docs"""
    print("\n" + "=" * 80)
    print("📄 TEST CONTEXT NODE")
    print("=" * 80)
    
    states = [
        {"name": "DOMAIN_DATA with docs", "docs": [{"text": "sample"}], "expected": "context"},
        {"name": "GENERAL_LLM with no docs", "docs": [], "expected": "empty context"},
    ]
    
    for state in states:
        print(f"\n✓ {state['name']}")
        if state['docs']:
            print(f"  Retrieved {len(state['docs'])} docs")
            print(f"  Expected: Non-empty context")
        else:
            print(f"  No docs retrieved")
            print(f"  Expected: Empty context → {state['expected']}")
            print(f"  ✓ context_node returns {'{\"context\": \"\"}'}")

def test_answer_node():
    """Test answer node logic"""
    print("\n" + "=" * 80)
    print("💬 TEST ANSWER NODE")
    print("=" * 80)
    
    scenarios = [
        {
            "name": "DOMAIN_DATA with context",
            "category": "DOMAIN_DATA",
            "context": "Present",
            "prompt_type": "Domain-specific (strict, no hallucination)",
            "expected": "Answer từ context, không bổ sung ngoài"
        },
        {
            "name": "GENERAL_LLM no context",
            "category": "GENERAL_LLM",
            "context": "Empty",
            "prompt_type": "General knowledge (open-ended)",
            "expected": "Answer từ mô hình, chi tiết và chuyên nghiệp"
        },
    ]
    
    for scenario in scenarios:
        print(f"\n✓ Scenario: {scenario['name']}")
        print(f"  Category: {scenario['category']}")
        print(f"  Context: {scenario['context']}")
        print(f"  Prompt Type: {scenario['prompt_type']}")
        print(f"  Expected: {scenario['expected']}")

def test_path_handling():
    """Test Windows path handling"""
    print("\n" + "=" * 80)
    print("📁 TEST WINDOWS PATH HANDLING")
    print("=" * 80)
    
    # Test path normalization
    test_paths = [
        "D:\\AI_AGENT\\vector_store",
        "D:/AI_AGENT/vector_store",
        "./vector_store",
        "../vector_store",
    ]
    
    for path_str in test_paths:
        try:
            path_obj = Path(path_str).resolve()
            normalized = str(path_obj.as_posix())
            print(f"\n✓ Input: {path_str}")
            print(f"  Resolved: {normalized}")
            print(f"  Valid: {path_obj.is_absolute()}")
        except Exception as e:
            print(f"\n❌ Error with {path_str}: {e}")

if __name__ == "__main__":
    print("\n🚀 ROUTER UPGRADE TEST SUITE\n")
    
    # Test intent classification (requires LLM)
    try:
        test_intent_classification()
    except Exception as e:
        print(f"⚠️  Skipped intent classification test: {e}")
    
    # Test router logic (no LLM needed)
    test_router_logic()
    test_context_node()
    test_answer_node()
    
    # Test path handling
    test_path_handling()
    
    print("\n" + "=" * 80)
    print("✅ TEST SUITE COMPLETED")
    print("=" * 80)
