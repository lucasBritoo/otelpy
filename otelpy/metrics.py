from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter as OTLgrpcExporter
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.metrics import get_meter_provider,set_meter_provider
from opentelemetry.sdk.metrics import MeterProvider, Meter
from opentelemetry.sdk.resources import Resource
from enum import Enum
from otelpy import loggerConfig
import os

logger = loggerConfig.get_logger('otelpy.metrics')

class MetricsCounter(Enum):
    pass

class MetricsHistogram(Enum):
    pass

class MetricsGauge(Enum):
    pass
    
class MetricsProvider():
    
    def __init__(self, resource_attributes_dict, grpc, metrics_exporter_url, **kwargs):
        self.meter: Meter = None
        self.resource_attributes_dict = resource_attributes_dict
        self.metrics_exporter_url = metrics_exporter_url
        self.grpc = grpc
        self.meter_name = os.environ['SERVICE_NAME']
        self.meter_version = os.environ['SERVICE_VERSION']
        self.setMetricsProvider()
        self.setMeter()
                
    def setMetricsProvider(self):
        
        resource = Resource.create(attributes=self.resource_attributes_dict)
        
        if self.grpc:
            logger.debug("Configurando OTLP GRPC Metrics Exporter")
            exporter = OTLgrpcExporter(endpoint=self.metrics_exporter_url,insecure=True)

        reader = PeriodicExportingMetricReader(exporter)
        provider = MeterProvider(resource=resource, metric_readers=[reader])
        set_meter_provider(provider)

    def setMeter(self):
        self.meter = get_meter_provider().get_meter(self.meter_name, self.meter_version)

class Metrics():
    
    def __init__(self, resources_dict):
        self.meter = self.config_provider(resources_dict=resources_dict)
        self.metrics = {}
        
        if self.should_instrumentation():
            self.create_metrics_counter()
            self.create_metric_histogram()
            self.create_metric_gauge()
    
    def create_metrics_counter(self):
        logger.debug("Creating counter metrics")
        for metric in MetricsCounter:
            self.metrics[metric.name] = self.meter.create_counter(
                name=metric.name,
                description=metric.value,
                unit='number'
            )
    
    def create_metric_histogram(self):
        logger.debug("Creating histogram metrics")
        for metric in MetricsHistogram:
            self.metrics[metric.name] = self.meter.create_histogram(
                name=metric.name,
                description=metric.value,
                unit='s'
            )

    def create_metric_gauge(self):
        # logger.debug("Creating gauge metrics")
        for metric in MetricsGauge:
            self.metrics[metric.name] = self.meter.create_gauge(
                name=metric.name,
                description=metric.value,
                unit='u'
            )
            
    def add_counter(self, metric_name, counter, labels):
        if self.should_instrumentation():
            self.metrics[metric_name].add(counter, labels)
    
    def add_histogram(self, metric_name, value, labels):
        if self.should_instrumentation():
            self.metrics[metric_name].record(value, labels)
            
    def add_gauge(self, metric_name, value, labels):
        if self.should_instrumentation():
            self.metrics[metric_name].set(value, labels)
        
    def config_provider(self, resources_dict):
        if self.should_instrumentation():
            metric_provider = MetricsProvider(
                resource_attributes_dict=resources_dict,
                grpc=True,
                metrics_exporter_url=os.environ['OTLP_METRICS_HOST']
            )
            return metric_provider.meter
    
    def should_instrumentation(self):
        return (
            os.getenv("OTLP_METRICS_DISABLE") or "false"
        ).lower() == "false"