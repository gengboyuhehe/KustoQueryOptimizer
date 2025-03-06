#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from kusto_query_performance_optimization.crew import KustoQueryPerformanceOptimization

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
"original_query": """
let performanceReport = ()
{
    chatReport()
    | union conversationReport()
    | union workflowReport()
    | union chatPanelReport()
};
performanceReport()
| where _userType !~ "consumer" or (Feature !contains "3S" and Feature !~ "Chat (CIQ)")
| where Feature !in ("Undefined", "fixAll_spellingAndGrammar", "Unknown") and isnotempty(Feature)
};
L1Unioned
| where App_Name == "Word"
    """,
    "target": 20
    }
    try:
        KustoQueryPerformanceOptimization().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        KustoQueryPerformanceOptimization().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        KustoQueryPerformanceOptimization().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        KustoQueryPerformanceOptimization().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
