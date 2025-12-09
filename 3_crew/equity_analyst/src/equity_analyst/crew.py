from inspect import trace
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from pydantic import BaseModel,Field
from crewai_tools import SerperDevTool

from crewai.memory import LongTermMemory,ShortTermMemory,EntityMemory
from crewai.memory.storage.rag_storage import RAGStorage
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage


# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators
class TrendingCompany(BaseModel):
    """A company in the news attractig attention"""
    name:str = Field(description = "Company Name")
    ticker:str = Field(description ="Stock ticker symbol")
    reason:str = Field(description = "Reason this company is trending in the news")

class TrendingCompanyList(BaseModel):
    """List of mutiple trending companies in the news"""
    companies:List[TrendingCompany]=Field(description="List of companies trending in the news")

class TrendingCompanyResearch(BaseModel):
    """Detailed research on a company"""
    name:str=Field(description="Company name")
    market_position:str=Field(description="Current market position and competitive analysis")
    future_outlook:str=Field(description="Future outlook and growth prospects")
    investment_potential:str=Field(description="Investment potential and suitability for investment")

class TrendingCompanyResearchList(BaseModel):
    """List of detailed research on all the companies"""
    companies:List[TrendingCompanyResearch]=Field(descripttion="Comprehensive research on all trending companies")


@CrewBase
class EquityAnalyst():
    """EquityAnalyst crew"""

    agents_config='config/agents.yaml'
    tasks_config='config/tasks.yaml'

    
    @agent
    def trending_company_finder(self) -> Agent:
        return Agent(
            config=self.agents_config['trending_company_finder'],tools=[SerperDevTool()]) # type: ignore[index]
            

    @agent
    def financial_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['financial_researcher'],tools=[SerperDevTool()]) # type: ignore[index]
    
    @agent
    def stock_picker(self) -> Agent:
            return Agent(
                config=self.agents_config['stock_picker'],memory=True)
        

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def find_trending_companies(self) -> Task:
        return Task(
            config=self.tasks_config['find_trending_companies'],
            output_pydantic=TrendingCompanyList # type: ignore[index]
        )

    @task
    def research_trending_companies(self) -> Task:
        return Task(
            config=self.tasks_config['research_trending_companies'], # type: ignore[index]
            output_pydantic=TrendingCompanyResearchList
        )
    @task
    def pick_best_companies(self) -> Task:
        return Task(
            config=self.tasks_config['pick_best_company'], # type: ignore[index]
            output_pydantic=TrendingCompanyResearch
        )
    @crew
    def crew(self) -> Crew:
        """Creates the EquityAnalyst crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge
        manager= Agent(
            config=self.agents_config['manager'],
            allow_delegation=True,
            tracing=True
        )
        short_term_memory=ShortTermMemory(
            storage=RAGStorage(
                embedder_config={
                    "provider":"openai",
                    "config":{
                        "model":"text-embedding-3-small"
                    }
                },
                type="short_term",
                path="./memory/"
            )
        )

        long_term_memory=LongTermMemory(
            storage=LTMSQLiteStorage(
                db_path="./memory/long_term_memory_storage.db"
            )
        )

        entity_memory = EntityMemory(
            storage=RAGStorage(
                embedder_config={
                    "provider":"openai",
                    "config":{
                        "model":"text-embedding-3-small"
                    }
                },
                type="short_term",
                path="./memory/"
            )
        )

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.hierarchical,
            verbose=True,
            manager_agent=manager,
            memory=True,
            long_term_memory=long_term_memory,
            short_term_memory=short_term_memory,
            entity_memory=entity_memory
        )
