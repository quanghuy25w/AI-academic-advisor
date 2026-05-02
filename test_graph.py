import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.agent.graph import graph

def main():
    initial_state = {
        "question": "Công nghệ điện toán đám mây",
        "rewritten_question": "",
        "intent": "",
        "plan": "",
        "retrieved_docs": [],
        "context": "",
        "answer": "",
        "reflection": "",
        "student_profile": {},
        "messages": [],
        "validation_result": {},
        "regenerate_count": 0,
        "skip_pipeline": False
    }
    
    result = graph.invoke(initial_state)
    
    print("Câu hỏi:", result["question"])
    print("\nCâu trả lời:", result["answer"])
    # Bạn có thể in thêm reflection nếu muốn
    # print("\nReflection:", result.get("reflection"))

if __name__ == "__main__":
    main()