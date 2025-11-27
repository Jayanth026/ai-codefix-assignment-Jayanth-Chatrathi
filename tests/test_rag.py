from app.rag import SimpleRAGRetriever


def test_rag_retrieval():
    rag = SimpleRAGRetriever(recipes_dir="recipes")
    rag.init()
    result = rag.retrieve("SQL injection in Java code with user input")
    assert result is None or isinstance(result[0], str)
