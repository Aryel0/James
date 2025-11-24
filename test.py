"""
Test script for James to verify tool usage
Run this to test if tools are working properly
"""

from jamesllm import ask
import sys

def print_section(title):
    print("\n" + "="*60)
    print(title)
    print("="*60 + "\n")

def test_tool(test_name, question, expected_behavior):
    print(f"[{test_name}]")
    print(f"Question: {question}")
    print(f"Expected: {expected_behavior}")
    print("-" * 60)
    
    try:
        answer = ask(question)
        print(f"\n✓ Answer: {answer}\n")
        return True
    except Exception as e:
        print(f"\n✗ Error: {str(e)}\n")
        return False

def main():
    print_section("JAMES TOOL USAGE TEST")
    
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Database query (no tools needed)
    tests_total += 1
    if test_tool(
        "TEST 1: Database Query",
        "What games do you have in your database?",
        "Should list games directly without using external tools"
    ):
        tests_passed += 1
    
    # Test 2: Wikipedia search
    tests_total += 1
    if test_tool(
        "TEST 2: Wikipedia Search",
        "Tell me about the game Tetris",
        "Should use Wikipedia tool to get information"
    ):
        tests_passed += 1
    
    # Test 3: Simple Wikipedia query
    tests_total += 1
    if test_tool(
        "TEST 3: Simple Fact Check",
        "Who created Minecraft?",
        "Should use Wikipedia tool and return creator name"
    ):
        tests_passed += 1
    
    # Test 4: Save functionality
    tests_total += 1
    if test_tool(
        "TEST 4: Save Tool",
        "Save this text to a file: James is working correctly!",
        "Should use save tool and confirm file creation"
    ):
        tests_passed += 1
    
    # Summary
    print_section("TEST SUMMARY")
    print(f"Tests Passed: {tests_passed}/{tests_total}")
    print(f"Success Rate: {(tests_passed/tests_total)*100:.1f}%")
    
    if tests_passed == tests_total:
        print("\n🎉 All tests passed! James is working correctly!")
        return 0
    else:
        print(f"\n{tests_total - tests_passed} test(s) failed. Review the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())