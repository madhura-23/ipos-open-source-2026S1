from datetime import timezone
from app.shared.event_hook import EventHook, NullEventHook, ProcessEvent


def test_process_event_defaults():
    event = ProcessEvent(name="task.completed")
    assert event.name == "task.completed"
    assert event.payload == {}
    assert event.timestamp.tzinfo == timezone.utc


def test_process_event_with_payload():
    event = ProcessEvent(name="task.failed", payload={"reason": "timeout"})
    assert event.payload["reason"] == "timeout"


def test_null_event_hook_handles_without_error():
    hook = NullEventHook()
    event = ProcessEvent(name="process.started", payload={"id": 42})
    hook.handle(event)  # should not raise


def test_event_hook_is_abstract():
    import pytest
    with pytest.raises(TypeError):
        EventHook()  # cannot instantiate abstract class


def test_custom_hook_receives_event():
    received = []

    class TestHook(EventHook):
        def handle(self, event: ProcessEvent) -> None:
            received.append(event)

    hook = TestHook()
    event = ProcessEvent(name="order.updated", payload={"order_id": 1})
    hook.handle(event)

    assert len(received) == 1
    assert received[0].name == "order.updated"
