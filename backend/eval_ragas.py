import os
import requests
import google.generativeai as genai
from dotenv import load_dotenv
import pandas as pd

# Load env
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
api_key = os.environ.get("GEMINI_API_KEY", "")

if not api_key:
    print("Warning: GEMINI_API_KEY not found in .env")
    exit(1)

genai.configure(api_key=api_key)
eval_model = genai.GenerativeModel("gemini-3.5-flash-lite")

def run_evals():
    print("Starting Requirement-Driven Evaluations on /api/chat...\n")
    
    # These map exactly to the user requirements for the Decision Pack
    test_suite = [
        {
            "query": "What is the capital expenditure for Option A?",
            "expected_trait": "Provenance: Traces to a specific document and page",
            "prompt": "Does this answer contain a specific document name and page number citation? Answer YES or NO."
        },
        {
            "query": "What are the comparable rates for Eastern Creek?",
            "expected_trait": "Trap 1: Reject unsourced comparable figures",
            "prompt": "Does this answer explicitly state that the comparable rate has NO ADMISSIBLE SOURCE and is excluded? Answer YES or NO."
        },
        {
            "query": "What is the outgoings recovery percentage?",
            "expected_trait": "Trap 2: Identify conflicts without silently resolving",
            "prompt": "Does this answer identify a conflict (e.g. between 92% and 88%) and explicitly state that a human must resolve it? Answer YES or NO."
        },
        {
            "query": "What is the verified passing income for Option B?",
            "expected_trait": "Trap 3: Coverage gap explicitly stated",
            "prompt": "Does this answer state that a portion of the income (279,531) is unverified due to a coverage gap? Answer YES or NO."
        },
        {
            "query": "Should we buy Option A or Option B?",
            "expected_trait": "Rule 5: No recommendation",
            "prompt": "Does this answer abstain from making a recommendation or state that it is under consideration without choosing one? Answer YES or NO."
        },
        {
            "query": "What is the value of Property Z?",
            "expected_trait": "Rule 3: Honest abstention when missing",
            "prompt": "Does this answer explicitly state that it must abstain, or that the query is out of context/blocked? Answer YES or NO."
        }
    ]
    
    api_url = "http://127.0.0.1:8005/api/chat"
    results = []
    
    for test in test_suite:
        print(f"Testing Query: '{test['query']}'")
        try:
            resp = requests.post(api_url, json={"message": test['query']}, timeout=30)
            ans = resp.json().get("response", "")
            
            # Use Gemini to judge if the response meets the strict requirement
            judge_prompt = f"Requirement: {test['prompt']}\n\nSystem Answer: {ans}\n\nDecision (YES/NO):"
            judge_resp = eval_model.generate_content(judge_prompt).text.strip()
            
            passed = "YES" in judge_resp.upper()
            
            print(f"  [Answer]: {ans}")
            print(f"  [Judge]: {judge_resp}")
            
            results.append({
                "Requirement": test["expected_trait"],
                "Query": test["query"],
                "Pass": passed,
                "Answer": ans[:75] + "..."
            })
            
        except Exception as e:
            print(f"Failed to query {api_url}: {e}")
            return
            
    df = pd.DataFrame(results)
    print("\n--- Evaluation Results ---")
    print(df[['Requirement', 'Pass', 'Query']].to_markdown(index=False))
    
    score = sum(df['Pass']) / len(df) * 100
    print(f"\nOverall Requirement Adherence Score: {score}%")

if __name__ == "__main__":
    run_evals()
