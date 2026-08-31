from agents.retriever_agent import RetrieverAgent
from agents.analyst_agent import AnalystAgent
from agents.answer_agent import AnswerAgent
import config


class Orchestrator:
    def __init__(self, vector_db):
        self.retriever_agent = RetrieverAgent(vector_db)
        self.analyst_agent = AnalystAgent(self.retriever_agent)
        self.answer_agent = AnswerAgent()
        self.history = []

    def ask(self, question, document_filter=None):
        result = self.analyst_agent.run(
            question,
            self.history,
            document_filter,
            config.MAX_FEEDBACK_LOOPS,
            config.TOP_K_RETRIEVE,
            config.TOP_K_FINAL
        )
        final = self.answer_agent.generate(question, result)
        self.history.append({"role": "user", "content": question})
        self.history.append({"role": "assistant", "content": final["answer"]})
        return final
