from fastapi import Request, Response
import os
import uuid
import logging
import ujson as json
from contextvars import ContextVar

trace_id_var: ContextVar[str] = ContextVar("trace_id", default=None)

class TraceIDFilter(logging.Filter):
    def filter(self, record) -> bool:
        trace_id = trace_id_var.get()
        record.trace_id = trace_id
        return True

class JsonFormatter(logging.Formatter):
    def format(self, record) -> str:
        log_record = {
            "trace_id": record.trace_id,
            "timestamp": self.formatTime(record),
            "message": record.getMessage(),
        }
        return json.dumps(log_record)

def setup() -> None:
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    formatter = JsonFormatter()

    if os.environ.get("K_SERVICE"):
        from google.cloud.logging_v2 import Client
        from google.cloud.logging_v2.handlers import CloudLoggingHandler
        client = Client()
        handler = CloudLoggingHandler(client)
    else:
        handler = logging.StreamHandler()
        
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
    root_logger.addFilter(TraceIDFilter())


# Middleware to capture trace id from incoming request
# Google Cloud Run sets the trace id in the 'X-Cloud-Trace-Context' header
async def setup_trace_id(request: Request, call_next) -> Response:
    trace_id = request.headers.get('X-Cloud-Trace-Context', uuid.uuid4().hex).split('/')[0]
    trace_id_var.set(trace_id)
    response = await call_next(request)
    return response