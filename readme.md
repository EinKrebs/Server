This is library for creating servers.

To create a server, create an instance of server.Server, then specify its functions and call its start() method.

<h3>Server functions:</h3>

All server functions work by decorators wrapping function f(request)  
In all decorators there are parameters addr for address of the page and host,
which can specify Host header needed to reach the page. 

1) decorator server.text(addr, host=None): 
   creates page with text returned by function;
2) decorator server.file(addr, host=None, const=False):
   creates page with file, whose name is returned by function. If 
   parameter const is True, then function must not depend on request, and value is
   being calculated when declaring function;
3) decorator server.directory_listing(addr, host=None, view=None):
   if view is None, creates page with names of files and directories in directory returned by function,
   else creates list of result of view(file_name) for every file and directory.
4) decorator server.custom_handler(addr, host=None):
   it just returns function result. For correct work, this result must be instance of HttpResponce class
   
<h3>Requests</h3>

Http requests are represented by class request.http_request.HttpRequest.
params, headers and cookies are represented by dictionaries, method by enum request.request_method.Method,
address by string

<h3>Responses</h3>

Http responses are represented by class response.http_response.HttpResponse

HttpResponse(code: Code, text_data: bytes = None, file: str = None):  
1) code - response code, instance of response.response_code.Code, which currently has 
only OK and PAGE_NOT_FOUND values;
2) text_data - if isn't None, response will contain this data, marked as text/html;
3) file - if text_data is None and this param is not None, response will contain 
content of file with name specified by param value
