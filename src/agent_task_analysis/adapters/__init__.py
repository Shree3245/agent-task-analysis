from importlib import import_module

SOURCES = (
    "otel",
    "langfuse",
    "langsmith",
    "litellm",
    "mini-swe-agent",
    "swe-agent",
    "openhands",
    "hal",
    "csv",
    "braintrust",
)


def adapter(source):
    return import_module("agent_task_analysis.adapters." + source.replace("-", "_")).extract
