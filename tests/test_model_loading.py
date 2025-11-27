from app.model import CodeFixModel


def test_model_loading():
    model = CodeFixModel()
    # To keep CI light you might want to mock this; but for assignment, we actually call it.
    model.load()
    assert model.pipe is not None
    assert model.tokenizer is not None
