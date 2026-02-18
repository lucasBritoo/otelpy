from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter as OTLPgrpcExporter

from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource
import logging
import os

LOG_FORMAT_DEFAULT = "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] - %(message)s"

class Logger():
    
    def __init__(self, **kwargs):
        # logging.debug('Config Logging')
        self.logger_name: str = kwargs['logger_name']
        self.log_level: str = kwargs['log_level']
        self.resources_dict: dict = kwargs['resources_dict']
        self.logs_exporter_url: str = kwargs['logs_exporter_url']
        self.handlers = []
        self.formatter = ""
        
        if self.should_instrumentation():
            self.setLogExporter()
            
        self.setLogConsole()
        self.setFormatter()
        self.setBasicConfig()
        self.setFilters()

    def get_logger(self, name):
        return logging.getLogger(name)
    
    def getConfig(self):
        return logging.basicConfig(level=logging.DEBUG,
                                   handlers=self.handlers,
                                   format=self.formatter)

    def setBasicConfig(self):
        self.getConfig()
    
    def getExporterHandler(self, url, grpc):
        logger_provider = LoggerProvider(resource=Resource.create(self.resources_dict))
        set_logger_provider(logger_provider)
        
        if grpc:
            otlp_exporter = OTLPgrpcExporter(endpoint=url, insecure=True)

        logger_provider.add_log_record_processor(BatchLogRecordProcessor(otlp_exporter))

        return LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)
    
    def getFileHandler(self, path):
        return logging.FileHandler(path)

    def getConsoleHandler(self):
        return logging.StreamHandler()
        
    def setLogFile(self, path: str= '/log.log'):
        self.handlers.append(self.getFileHandler(path))
        
    def setLogExporter(self):
        self.handlers.append(
            self.getExporterHandler(
                self.logs_exporter_url,
                grpc=True
            )
        )
        
    def setLogConsole(self):
        self.handlers.append(self.getConsoleHandler())

    def setFormatter(self, formatter: str=LOG_FORMAT_DEFAULT):
        self.formatter = formatter

    def setFilters(self):
        pass

    def should_instrumentation(self):
        return (
            os.getenv("OTLP_LOGGING_DISABLE") or "false"
        ).lower() == "false"
