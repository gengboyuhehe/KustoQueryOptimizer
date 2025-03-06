from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from kusto_query_performance_optimization.tools.custom_tool import PerformanceTestTool

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class KustoQueryPerformanceOptimization():
	"""KustoQueryPerformanceOptimization crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'
	# llm = LLM(
	# 	model='openai/glm-4-plus',
	# 	base_url='https://open.bigmodel.cn/api/paas/v4/',
	# 	api_key='******'
	# )
	# llmLight = LLM(
	# 	model='openai/glm-4-flash',
	# 	base_url='https://open.bigmodel.cn/api/paas/v4/',
	# 	api_key='******'
	# )

	llmGpt = LLM(
		model = "azure/gpt-4o",
		base_url='******',
		api_key='**********'
	)


	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def optimizer(self) -> Agent:
		return Agent(
			config=self.agents_config['optimizer'],
			verbose=True,
			tools=[PerformanceTestTool()],
			llm=self.llmGpt
		)
	# @agent
	# def tester(self) -> Agent:
	# 	return Agent(
	# 		config=self.agents_config['tester'],
	# 		verbose=True,
	# 		tools=[PerformanceTestTool()],
	# 		llm=self.llmGpt)

	# def manager(self) -> Agent:
	# 	return Agent(
	# 		config=self.agents_config['manager'],
	# 		verbose=True,
	# 		llm=self.llmGpt,
	# 		allow_delegation=True)
	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def optimize_query_task(self) -> Task:
		return Task(
			config=self.tasks_config['optimize_query_task'],
		)
	
	# @task
	# def optimize_query_task(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['optimize_query_task'],
	# 		#output_file='optimized_query.kql'
	# 	)

	# @task
	# def test_query_task(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['test_query_task'],
	# 		#output_file='test_result.json'
	# 	)
	

	# @task
	# def optimize_intern_query_task(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['optimize_intern_query_task'],
	# 	)
	@crew
	def crew(self) -> Crew:
		"""Creates the KustoQueryPerformanceOptimization crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# manager_agent=self.manager()
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)