from lepotato_hmi.emotions import EmotionEngine
from lepotato_hmi.events import Event, EventBus


def test_bounded_bus_keeps_latest():
    bus = EventBus(capacity=2)
    for index in range(3):
        bus.publish(Event.build("test.passed", "test", {"index": index}))
    assert [event.payload["index"] for event in bus.history] == [1, 2]


def test_subscribers_are_independent():
    bus = EventBus()
    first, second = bus.subscribe(1), bus.subscribe(1)
    for index in range(2):
        bus.publish(Event.build("sample", "test", {"index": index}))
    assert first.get_nowait().payload["index"] == 1
    assert second.get_nowait().payload["index"] == 1


def test_emotion_mapping():
    engine = EmotionEngine()
    assert engine.apply(Event.build("test.passed", "test", {})).mood == "happy"
    assert engine.apply(Event.build("test.failed", "test", {})).mood == "concerned"
