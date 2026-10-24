from moira.classify import classify_task
from moira.schema import Task, Call


def test_explicit_type_preserved_and_rules_use_only_metadata():
    task = Task(
        "a", task_type="customer_case", calls=[Call("a", 0, event_kind="tool", tool_name="shell")]
    )
    assert classify_task(task) == "customer_case"
    task.task_type = "unknown"
    assert classify_task(task) == "code"
    task = Task("b", n_calls=1)
    assert classify_task(task) == "unknown"
