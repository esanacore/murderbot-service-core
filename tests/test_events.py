from murderbot_core.events import Event, EventBus, EventType


def test_publish_calls_subscribed_handler() -> None:
    bus = EventBus()
    received: list[Event] = []
    bus.subscribe(EventType.MAIN_RAIL_ON, received.append)

    event = Event(type=EventType.MAIN_RAIL_ON)
    bus.publish(event)

    assert received == [event]


def test_publish_does_not_call_handlers_for_other_event_types() -> None:
    bus = EventBus()
    received: list[Event] = []
    bus.subscribe(EventType.MAIN_RAIL_ON, received.append)

    bus.publish(Event(type=EventType.MAIN_RAIL_OFF))

    assert received == []


def test_publish_with_no_subscribers_does_not_raise() -> None:
    bus = EventBus()
    bus.publish(Event(type=EventType.HOST_HEARTBEAT))


def test_unsubscribe_stops_delivery() -> None:
    bus = EventBus()
    received: list[Event] = []
    bus.subscribe(EventType.RESET_BUTTON, received.append)
    bus.unsubscribe(EventType.RESET_BUTTON, received.append)

    bus.publish(Event(type=EventType.RESET_BUTTON))

    assert received == []


def test_multiple_subscribers_all_receive_the_event() -> None:
    bus = EventBus()
    received_a: list[Event] = []
    received_b: list[Event] = []
    bus.subscribe(EventType.POWER_BUTTON, received_a.append)
    bus.subscribe(EventType.POWER_BUTTON, received_b.append)

    event = Event(type=EventType.POWER_BUTTON)
    bus.publish(event)

    assert received_a == [event]
    assert received_b == [event]


def test_event_payload_defaults_to_empty_dict() -> None:
    event = Event(type=EventType.TEMPERATURE_WARNING)
    assert event.payload == {}


def test_event_is_immutable() -> None:
    event = Event(type=EventType.MAIN_RAIL_ON)
    try:
        event.type = EventType.MAIN_RAIL_OFF  # type: ignore[misc]
    except AttributeError:
        pass
    else:
        raise AssertionError("Event should be frozen/immutable")
