import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from repository import all, retrieve, create, update, delete


class HandleRequests(BaseHTTPRequestHandler):
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """
    def parse_url(self, path):
        
        path_params = path.split("/")
        resource = path_params[1]
        id = None

        try:
            id = int(path_params[2])
        except IndexError:
            pass
        except ValueError:
            pass 

        return (resource, id)

    def get_all_or_single(self, resource, id):
        if id is not None:
            response = retrieve(resource, id)

            if response is not None:
                self._set_headers(200)
            else:
                self._set_headers(404)
                response = f'This {resource[:-1]} cannot be found'
        else:
            self._set_headers(200)
            response = all(resource)

        return response


    def do_GET(self):
        response = {}
        (resource, id) = self.parse_url(self.path)
        response = self.get_all_or_single(resource, id)
        self.wfile.write(json.dumps(response).encode())

        
    def do_POST(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)
        (resource, id) = self.parse_url(self.path)
        new_data = None

        if resource == "animals":
            if "name" in post_body and "species" in post_body and "locationId" in post_body and "customerId" in post_body and "status" in post_body:
                self._set_headers(201)
                new_data = create(resource, post_body)
            else:
                self._set_headers(400)
                new_data = {"message": f'{"Name is required" if "name" not in post_body else""} {"Species is required" if "species" not in post_body else ""} {"Location is required" if "locationId" not in post_body else ""} {"Customer is required" if "customerId" not in post_body else ""} {"Status is required" if "status" not in post_body else ""}'}

        elif resource == "locations":
            if "name" in post_body and "address" in post_body:
                self._set_headers(201)
                new_data = create(resource, post_body)
            else:
                self._set_headers(400)
                new_data = {
                "message": f'{"Name is required" if "name" not in post_body else ""} {"Address is required" if "address" not in post_body else ""}'}

        elif resource == "employees":
            if "name" in post_body:
                self._set_headers(201)
                new_data = create(resource, post_body)
            else:
                self._set_headers(400)
                new_data = {
                "message": f'{"Name is required" if "name" not in post_body else ""}'}

        elif resource == "customers":
            if "fullName" in post_body and "email" in post_body:
                self._set_headers(201)
                new_data = create(resource, post_body)
            else:
                self._set_headers(400)
                new_data = {
                "message": f'{"Name is required" if "fullName" not in post_body else ""} {"Email is required" if "email" not in post_body else ""}'}
        
        self.wfile.write(json.dumps(new_data).encode())

    def do_PUT(self):
        self._set_headers(204)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        (resource, id) = self.parse_url(self.path)
        update(resource, id, post_body)
        self.wfile.write("".encode())


    def do_DELETE(self):
        response = ""
        (resource, id) = self.parse_url(self.path)

        if resource == "customers":
            self._set_headers(405)
            response = {"message": "Deleting a customer requires contacting the company directly"}
        else:
            delete(resource, id)
            # Animal data is dependent on these locations so shouldn't fully delete
            if resource == "locations":
                self._set_headers(200)
            else:
                self._set_headers(204)
            
        self.wfile.write(response.encode())

    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()


# This function is not inside the class. It is the starting
# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
