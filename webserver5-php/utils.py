import io

def parse_http_request(raw_request):
    """return tuple of (method, url, request_body, request_header)"""
    ss = io.StringIO(raw_request)
    request = ss.readline()
    request_method, request_uri, http_version = request.strip().split(" ")
    request_headers = {}
    # read header
    while True:
        line = ss.readline().strip()

        if line:
            header, header_value = line.split(": ")
            request_headers[header] = header_value
        else: # empty line between header and body
            break
    request_body = ss.read()
    ss.close()
    return (request_method, request_uri, request_body, request_headers)

def encode_http_response(status_code, headers, body):
    status_code_desc = {
        200: "OK",
        201: "Created",
        202: "Accepted",
        203: "Non-Authoritative Information",
        204: "No Content",
        205: "Reset Content",
        206: "Partial Content",

        300: "Multiple Choices",
        301: "Moved Permanently",
        302: "Found",
        303: "See Other",
        304: "Not Modified",
        305: "Use Proxy",
        #306: "(Unused)",
        307: "Temporary Redirect",

        400: "Bad Request",
        401: "Unauthorized",
        402: "Payment Required",
        403: "Forbidden",
        404: "Not Found",
        405: "Method Not Allowed",
        406: "Not Acceptable",
        407: "Proxy Authentication Required",
        408: "Request Timeout",
        409: "Conflict",
        410: "Gone",
        411: "Length Required",
        412: "Precondition Failed",
        413: "Request Entity Too Large",
        414: "Request-URI Too Long",
        415: "Unsupported Media Type",
        416: "Requested Range Not Satisfiable",
        417: "Expectation Failed",

        500: "Internal Server Error",
        501: "Not Implemented",
        502: "Bad Gateway",
        503: "Service Unavailable",
        504: "Gateway Timeout",
        505: "HTTP Version Not Supported"
    }

    response = ""
    http_version = "HTTP/1.1"
    status_desc = status_code_desc[status_code]

    # write response status code
    response += "{0} {1} {2}\n".format(http_version, status_code, status_desc)
    # write headers
    for header, header_value in headers.items():
        response += "{0}: {1}\n".format(headers, header_value)
    response += "Content-length: {0}\n".format(len(body))
    response += "\n"
    # write body
    response += body

    return response
