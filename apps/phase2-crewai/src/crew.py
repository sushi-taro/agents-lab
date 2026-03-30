import os
from crewai import Agent, Task, Crew, LLM, Process
from crewai.project import CrewBase, agent, task, crew
from tools import search_tool

@CrewBase
class JleagueCrew:

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def _llm(self):
        return LLM(
            model="gemini/gemini-3.1-flash-lite-preview",
            api_key=os.environ["GEMINI_API_KEY"],
            temperature=0.3,
        )

    # Agent
    @agent
    def collector(self) -> Agent:
        return Agent(
            config=self.agents_config["collector"],
            tools=[search_tool],
            llm=self._llm(),
            verbose=True,
        )

    @agent
    def analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["analyst"],
            llm=self._llm(),
            verbose=True,
        )

    @agent
    def writer(self) -> Agent:
        return Agent(
            config=self.agents_config["writer"],
            llm=self._llm(),
            verbose=True,
        )

    @agent
    def reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config["reviewer"],
            llm=self._llm(),
            verbose=True,
        )

    # Task: 「何をするか」をAgentから分離して定義する
    @task
    def collect_task(self) -> Task:
        return Task(
            config=self.tasks_config["collect_task"],
        )

    @task
    def analyze_task(self) -> Task:
        return Task(
            config=self.tasks_config["analyze_task"],
            context=[self.collect_task()],
        )

    @task
    def write_task(self) -> Task:
        return Task(
            config=self.tasks_config["write_task"],
            context=[self.collect_task(), self.analyze_task()],
        )

    @task
    def review_task(self) -> Task:
        return Task(
            config=self.tasks_config["review_task"],
            context=[self.collect_task(), self.write_task()],
        )

    # Crew
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

# モジュールレベルでインスタンスを生成（main.pyからimportするため）
jleague_crew = JleagueCrew().crew()