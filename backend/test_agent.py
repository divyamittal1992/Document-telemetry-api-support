from agent.agent import build_agent

print("=== Phase 3: Agent Test ===\n")
print("Building agent...")
agent = build_agent()
print("Agent ready.\n")

# Test questions — these exercise different tools and reasoning paths
questions = [
    "What is an ANR and how does Android detect it?",
    "How do I monitor battery usage on Android?",
    "Compare how Android and iOS handle performance monitoring",
]

for question in questions:
    print(f"\n{'='*50}")
    print(f"Question: {question}")
    print('='*50)

    result = agent.invoke({
        "input": question,
        "chat_history": []   # Empty for now — we add memory in Phase 4
    })

    print(f"\nAnswer: {result['output']}")
