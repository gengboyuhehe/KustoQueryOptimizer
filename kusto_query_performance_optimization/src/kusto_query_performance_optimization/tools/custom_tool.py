from crewai.tools import BaseTool
from typing import Type,Dict
from pydantic import BaseModel, Field
import random


# class AccuracyTestToolInput(BaseModel):
#     """Input schema for AccuracyTestToolInput."""
#     argument: Dict = Field(..., description="Put the original query into the 'original_query' key and the optimized query into the 'optimized_query' key. And make sure these two key value pairs are wrapped in inside 'argument' key.")

# class AccuracyTestTool(BaseTool):
#     name: str = "accuracy_test_tool"
#     description: str = (
#         "Compare the output of original and optimized queries and return whether they are the nearly same."
#     )
#     args_schema: Type[BaseModel] = AccuracyTestToolInput

#     def _run(self, argument: str) -> str:
#         _=argument.get('original_query',"")
#         _=argument.get('optimized_query',"")
#         # Implementation goes here
#         return True
#     def _get_tool(self):
#         return AccuracyTestTool()

class PerformanceTestToolInput(BaseModel):
    """Input schema for PerformanceTestTool."""
    argument: Dict = Field(..., description="Put the query into the 'input_query' key. And make sure the key value pair is wrapped in inside 'argument' key.")

class PerformanceTestTool(BaseTool):
    name: str = "performance_test_tool"
    description: str = (
        "Get the execution time and the accuracy of the input kusto query. The output will be a dict in the format of {'execution_time':int,'accuracy':bool}."
    )
    
    args_schema: Type[BaseModel] = PerformanceTestToolInput

    def _run(self, argument: str) -> Dict[str,any]:
        _ = argument.get("input_query","")
        # Implementation goes here
        return {'execution_time':random.randint(30,100),'accuracy':True}
    
    def _get_tool(self):
        return PerformanceTestTool()

class ReadFileToolInput(BaseModel):
    """Input schema for ReadFileTool."""
    argument: Dict = Field(..., description="Put the file path into the 'file_path' key. And make sure the key value pair is wrapped in inside 'argument' key.")

class ReadFileTool(BaseTool):
    name: str = "read_file_tool"
    description: str = (
        "Read the content of the file given the file path. The output will be the content of the file."
    )
    args_schema: Type[BaseModel] = ReadFileToolInput

    def _run(self, argument: str) -> str:
        path = argument.get("file_path","")
        with open(path,'r') as file:
            content = file.read()
            return content