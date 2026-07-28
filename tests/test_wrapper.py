from src.wrapper import ProductionLLMWrapper

def test_wrapper_initialization():
    wrapper = ProductionLLMWrapper(api_key="test-key", model="gpt-4o-mini")
    assert wrapper.model == "gpt-4o-mini"
    assert wrapper.api_key == "test-key"
