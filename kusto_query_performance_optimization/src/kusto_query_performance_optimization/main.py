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
    | join kind=leftouter BizChatL1
        on $left.Feature == $right.Scenario
    | extend BizChatFCFR = tostring(round(BizChatFCFR/1000.0,2)), BizChatLCFR = tostring(round(BizChatLCFR/1000.0,2))
    | extend BizChatFCFR = iff(isempty(BizChatFCFR), 'N/A', BizChatFCFR)
    | extend BizChatLCFR = iff(isempty(BizChatLCFR), 'N/A', BizChatLCFR)
    | extend order = case (
        Feature == "Chat - Pane Ready to Interact", 10,
        Feature == "Chat - Pane Visually Ready", 11,
        Feature == "Chat - Pane Fully Load", 12,
        Feature == "Chat (Express/No RAG)", 13,
        Feature == "Chat (Doc Q&A)", 14,
        Feature == "Chat - 1 Iteration (3S, Web)", 15,
        Feature == "Chat - 1 Iteration (3S)", 16,
        Feature == "Chat - 1 Iteration (Web)", 17,
        Feature == "Chat - 1 Iteration (3S, Web, DocSearch)", 18,
        Feature == "Chat - 2 Iterations (3S, Web, DocSearch)", 19,
        Feature == "Chat - All Iterations (3S, Web, DocSearch)", 20,
        Feature == "Chat (CIQ)", 19,
        Feature == "Chat (CIQ - File Upload)", 20,
        Feature == "Chat (All up)", 21,
        Feature == "Chat - DQG", 31,
        99
    )
    | sort by App_Name, order asc, Feature asc
    | project App_Name, Feature, Volume=Count, FCFR, BizChatFCFR, LCFR, BizChatLCFR;
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
