from types import SimpleNamespace

from fastapi.testclient import TestClient
from langchain_core.documents import Document

from app.main import app
from app.services import chat_service

client = TestClient(app)


def test_chat_uses_retrieved_context_and_returns_sources(monkeypatch):
	class StubRetriever:
		def invoke(self, question):
			assert question == "How do retirement contributions work?"
			return [
				Document(
					page_content="The document explains retirement contributions.",
					metadata={"source": "/documents/retirement.pdf", "page": 1},
				)
			]

	class StubLLM:
		def invoke(self, messages):
			assert "retirement contributions" in messages[-1].content
			return SimpleNamespace(content="The document discusses contributions.")

	monkeypatch.setattr(chat_service, "get_retriever", lambda: StubRetriever())
	monkeypatch.setattr(chat_service, "get_llm", lambda: StubLLM())

	response = client.post(
		"/api/chat",
		json={"message": "How do retirement contributions work?"},
	)

	assert response.status_code == 200
	assert response.json()["candidates"][0]["content"]["parts"][0]["text"] == (
		"The document discusses contributions."
	)
	assert response.json()["sources"] == [{"file": "retirement.pdf", "page": 2}]


def test_chat_reports_missing_documents(monkeypatch):
	def missing_documents():
		raise FileNotFoundError("No PDF documents found")

	monkeypatch.setattr(chat_service, "get_retriever", missing_documents)

	response = client.post("/api/chat", json={"message": "What is in the file?"})

	assert response.status_code == 503
	assert response.json()["detail"] == "No PDF documents found"
