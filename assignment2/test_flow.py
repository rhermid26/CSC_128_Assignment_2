#your replay tests
# test_flow.py
from flow import handle, new_state


def replay(messages):
    """Run a whole conversation and hand back the final state."""
    state = new_state()
    replies = []
    for message in messages:
        reply, state = handle(message, state)
        replies.append(reply)
    return replies, state


replies, state = replay(["advising", "monday", "yes"])
assert state["stage"] == "done"
assert state["slot"] == "Monday 10:00 AM"

replies, state = replay(["advising", "monday", "start over"])
assert state["department"] is None

print("conversation tests passed")