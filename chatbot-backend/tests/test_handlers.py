import pytest
from v1.src.handler import TextHandler, ListenHandler, EndHandler, DeciderHandler, IntentHandler, QaHandler, AIHandler, ValidatorHandler, SetValueHandler, CounterHandler, IfHandler

@pytest.fixture
def vars():
    return {"last_utterance": "Hello"}

def test_text_handler():
    handler = TextHandler(text="Hi there!")
    text, intent = handler.execute()
    assert text == "Hi there!"
    assert intent is None

def test_listen_handler(vars):
    handler = ListenHandler()
    text, intent = handler.execute("Hello", vars=vars)
    assert text == "Hello" 
    assert intent is None

def test_end_handler():
    handler = EndHandler(text="Goodbye!")
    text, intent = handler.execute()
    assert text == "Goodbye!"
    assert intent is None
    
def test_decider_handler(vars):
    handler = DeciderHandler(labels=["greeting", "bye"])
    text, intent = handler.execute(vars=vars)
    assert intent == "greeting"
    assert text is None
    
def test_intent_handler():
    handler = IntentHandler(label="greeting")
    intent, text = handler.execute()
    assert intent == "greeting"
    assert text is None
    
@pytest.mark.parametrize("handler_class,expected", [
    (QaHandler, "success"), 
    (AIHandler, "success"),
    (ValidatorHandler, "valid"),
    ])
def test_success_handlers(handler_class, expected, vars):
    handler = handler_class()
    text, intent = handler.execute(vars=vars)
    assert intent == expected

def test_set_value_handler():
    handler = SetValueHandler(set_value="testing")
    value, intent = handler.execute()
    assert value == "testing"
    assert intent is None
    
def test_counter_handler(vars):
    handler = CounterHandler(add=2)
    value, intent = handler.execute(vars={"counter": 0})
    assert value == 2
    assert intent is None
    
@pytest.mark.parametrize("condition,expected", [
    ("contains", "yes"),
    ("not_contains", "no")   
])
def test_if_handler(condition, expected, vars):
    handler = IfHandler(condition=condition, variable="last_utterance", var_value="hello")
    value, intent = handler.execute(vars=vars)
    assert intent == expected