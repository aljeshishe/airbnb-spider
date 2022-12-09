import logging
from urllib.parse import urlunparse

import attrs
import scrapy
from scrapy import Request
from scrapy.exceptions import NotConfigured
from scrapy.http import Response
from scrapy.utils.httpobj import urlparse_cached
from scrapy.utils.python import to_bytes
from twisted.web import http

log = logging.getLogger(__name__)


@attrs.define
class LoggingDownloaderMiddleware:
    enabled: bool
    body_debug: bool

    @classmethod
    def from_crawler(cls, crawler):
        enabled = crawler.settings['REQUEST_RESPONSE_DEBUG']
        body_debug = crawler.settings.get("REQUEST_RESPONSE_BODY_DEBUG", False)
        return cls(enabled=enabled, body_debug=body_debug)

    def process_request(self, request, spider):
        self._sanitize(request=request)
        if self.enabled:
            repr = request_httprepr(request, body=self.body_debug)
            log.debug(f"Request:\n{repr}")
        return

    def process_response(self, request, response, spider):
        if self.enabled:
            repr = response_httprepr(response, body=self.body_debug)
            log.debug(f"Reponse:\n{repr}")
        return response

    def _sanitize(self, request: scrapy.Request):
        if "Content-Length" in request.headers:
            log.warning(f"Dont pass Content-Length header, it will be calculated automatically")

        encoding = request.headers.get("Accept-Encoding", "").decode()
        compression_enabled = any(tag in encoding for tag in ("gzip", "compress", "deflate", "br"))
        if compression_enabled:
            log.warning(f"Body compression (Accept-Encoding={encoding}) and printing body is enabled. Removing header")
            del request.headers["Accept-Encoding"]




def response_httprepr(response: Response, body: bool = False) -> str:
    """Return raw HTTP representation (as bytes) of the given response. This
    is provided only for reference, since it's not the exact stream of bytes
    that was received (that's not exposed by Twisted).
    """
    values = [
        b"HTTP/1.1 ",
        to_bytes(str(response.status)),
        b" ",
        to_bytes(http.RESPONSES.get(response.status, b'')),
        b"\r\n",
    ]
    if response.headers:
        values.extend([response.headers.to_string(), b"\r\n"])
    if body:
        values.extend([b"\r\n", response.body])
    return b"".join(values).decode("utf-8")


def request_httprepr(request: Request, body: bool = False) -> str:
    """Return the raw HTTP representation (as bytes) of the given request.
    This is provided only for reference since it's not the actual stream of
    bytes that will be send when performing the request (that's controlled
    by Twisted).
    """
    parsed = urlparse_cached(request)
    path = urlunparse(('', '', parsed.path or '/', parsed.params, parsed.query, ''))
    s = to_bytes(request.method) + b" " + to_bytes(path) + b" HTTP/1.1\r\n"
    s += b"Host: " + to_bytes(parsed.hostname or b'') + b"\r\n"
    if request.headers:
        s += request.headers.to_string() + b"\r\n"
    s += b"\r\n"
    if body:
        s += request.body
    return s.decode("utf-8")
