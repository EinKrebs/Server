This is library for creating servers.

To create a server, create an instance of server.Server and call its start() method.

Functions:
1) static text pages: created by creating function page(), which returns text to appear
on page, wrapped by server.text(addr) decorator, where addr is page url. 
