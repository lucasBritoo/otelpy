from otelpy.logging import Logger
from opentelemetry.sdk.resources import SERVICE_NAME, SERVICE_VERSION, SERVICE_NAMESPACE 
from dotenv import load_dotenv
import subprocess
import os
load_dotenv('/workspaces/gen-ai/.env')

def get_current_branch():
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return os.environ['SERVICE_NAMESPACE']
    except FileNotFoundError:
        return os.environ['SERVICE_NAMESPACE']

resources_dict = {
    SERVICE_NAME: os.environ['SERVICE_NAME'],
    SERVICE_VERSION: os.environ['SERVICE_VERSION'],
    SERVICE_NAMESPACE: get_current_branch()
}
provider = None

loggerConfig = Logger(
    logger_name=os.environ['SERVICE_NAME'],
    log_level=os.environ['OTLP_LOGGING_LEVEL'],
    resources_dict=resources_dict,
    logs_exporter_url=os.environ['OTLP_LOGGING_HOST']
)

from otelpy.traces import (
    Instrumentation,
    TraceInstruments,
    should_instrumentation,
    instrumented_trace,
    set_span_attribute
)
from otelpy.metrics import Metrics, MetricsCounter, MetricsHistogram, MetricsGauge

if should_instrumentation():
    instrumentor = Instrumentation(grpc=True, resource_attributes_dict=resources_dict, 
                    traces_exporter_url=os.environ['OTLP_TRACES_HOST'])
    provider = instrumentor.get_provider()
    
meter = Metrics(resources_dict=resources_dict)

__all__ = [
    "Instrumentation",
    "TraceInstruments",
    "should_instrumentation",
    "instrumented_trace",
    "meter",
    "provider",
    "MetricsCounter",
    "MetricsHistogram",
    "MetricsGauge"
]