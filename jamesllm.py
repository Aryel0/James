from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriver
import json 
from tools import TOOLS
import utils
import re

model = OllamaLLM(model="llama3.2")

template = utils.read_file("prompt.txt")

prompt_template = ChatPromptTemplate.from_template(template)
chain = prompt_template | model

def extract_json_from_response(response: str):
    """Extract JSON from response, handling cases where model adds extra text"""
    # Remove any markdown code blocks
    response = re.sub(r'```(?:json)?\s*', '', response)
    response = re.sub(r'```\s*', '', response)
    
    # Try to find JSON object (including nested braces)
    json_match = re.search(r'\{(?:[^{}]|(?:\{[^{}]*\}))*\}', response, re.DOTALL)
    if json_match:
        return json_match.group(0)
    
    return response.strip()

def format_games_context(games):
    """Format the retrieved games into a clear, readable list"""
    if not games:
        return "No games found in database."
    
    games_list = []
    for i, doc in enumerate(games, 1):
        title = doc.metadata.get('title', 'Unknown')
        author = doc.metadata.get('author', 'Unknown')
        year = doc.metadata.get('year', 'Unknown')
        games_list.append(f"{i}. {title} by {author} ({year})")
    
    return "\n".join(games_list)

def ask(question: str, max_loops=5):
    """
    Ask James a question with tool usage support
    
    Args:
        question: The user's question
        max_loops: Maximum number of tool calls before returning
    """
    # Retrieve relevant games from the database
    games = retriver.invoke(question)
    games_context = format_games_context(games)
    
    conversation_history = []
    input_text = {
        "games": games_context,
        "question": question,
        "history": ""
    }

    for loop_count in range(max_loops):
        response = chain.invoke(input_text).strip()
        print(f"\n[Loop {loop_count + 1}] Model response:")
        print(response)
        print()

        # Try to parse as tool call
        try:
            # Extract JSON from response
            json_str = extract_json_from_response(response)
            tool_call = json.loads(json_str)
            
            # Validate tool call structure
            if "tool" not in tool_call:
                raise ValueError("Response missing 'tool' field")
            
            tool_name = tool_call["tool"].lower()
            args = tool_call.get("args", {})

            # Handle final answer
            if tool_name == "final_answer":
                answer = args.get("answer", "")
                if answer:
                    return answer
                else:
                    # If empty answer, ask for a better response
                    conversation_history.append("Error: final_answer requires a non-empty 'answer' in args")
                    input_text["history"] = "\n\n".join(conversation_history)
                    continue

            # Handle tool calls
            if tool_name in TOOLS:
                print(f"[Calling tool: {tool_name} with args: {args}]")
                
                # Extract and call with the appropriate argument
                try:
                    if tool_name in ["search", "wikipedia"]:
                        if "query" in args:
                            result = TOOLS[tool_name](args["query"])
                        else:
                            result = f"Error: '{tool_name}' requires 'query' in args. Format: {{\"tool\": \"{tool_name}\", \"args\": {{\"query\": \"your query\"}}}}"
                    elif tool_name == "save":
                        if "text" in args:
                            result = TOOLS[tool_name](args["text"])
                        else:
                            result = f"Error: 'save' requires 'text' in args. Format: {{\"tool\": \"save\", \"args\": {{\"text\": \"your text\"}}}}"
                    else:
                        result = f"Error: Unknown argument structure for tool '{tool_name}'"
                except Exception as e:
                    result = f"Error calling tool '{tool_name}': {str(e)}"
                
                print(f"[Tool result: {result}]")
                
                # Add to conversation history
                conversation_history.append(
                    f"You called: {tool_name}\n"
                    f"Arguments: {args}\n"
                    f"Result: {result}"
                )
                
                # Update input with tool result
                input_text["history"] = "\n\n".join(conversation_history)
                input_text["question"] = (
                    f"Original question: {question}\n\n"
                    f"You just received this result from {tool_name}: {result}\n\n"
                    f"Now provide your final answer using the 'final_answer' tool."
                )
                continue
            else:
                # Unknown tool
                error_msg = (
                    f"Unknown tool: '{tool_name}'. "
                    f"Available tools are: {', '.join(TOOLS.keys())}, final_answer"
                )
                print(f"[{error_msg}]")
                conversation_history.append(f"Error: {error_msg}")
                input_text["history"] = "\n\n".join(conversation_history)
                continue

        except (json.JSONDecodeError, ValueError, KeyError) as e:
            # If we can't parse JSON, check if it looks like a natural response
            print(f"[Parsing error: {e}]")
            
            # If response is substantial and not JSON, treat it as a final answer
            if len(response) > 30 and not response.strip().startswith("{"):
                return response
            
            # Otherwise, provide guidance
            if loop_count < 2:
                conversation_history.append(
                    f"Error: Invalid JSON format. Your response must be valid JSON.\n"
                    f"Received: {response[:100]}...\n"
                    f"Required format: {{\"tool\": \"tool_name\", \"args\": {{...}}}}"
                )
                input_text["history"] = "\n\n".join(conversation_history)
                continue
            
            # Last resort: return what we have
            return response if len(response) > 20 else "I apologize, but I'm having trouble formatting my response correctly."

    return "I apologize, but I couldn't complete your request within the available steps. Please try rephrasing your question."