from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import parse_qs, urlsplit
import cgi
import sqlite3
from sqlite3 import Error
import json
def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print("The error '{e}' occurred")

    return connection
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query executed successfully")
    except OperationalError as e:
        print("The error '{e}' occurred")

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print("The error '{e}' occurred")

connection = create_connection("database")

create_users_table = """
CREATE TABLE IF NOT EXISTS users (
  message TEXT NOT NULL,
  sender TEXT,
  reciever TEXT
);
"""


execute_query(connection,create_users_table)
class GP(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
    
    
    def do_HEAD(self):
        self._set_headers()
    
    
    def do_GET(self):
        self._set_headers()
        print self.path
        
        params=parse_qs(self.path[2:])
        if 'user' in params:
            reciever = params['user'][0]
        print("LOOKING FOR: "+reciever)

        grabMessages= """
        SELECT sender, message 
        FROM users
        WHERE reciever='"""+reciever+"""'"""
        messages = execute_read_query(connection, grabMessages)
        print(messages)
        jsonFormatting= {"response":{"user":reciever,"messages": messages}}
        jsonFormatting = json.dumps(jsonFormatting)
        self.wfile.write("<html><body><h1>Get Request Received!</h1></body></html>")


    def do_POST(self):
        self._set_headers()
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'}
        )
        sender= form.getvalue("sender")
        reciever= form.getvalue("reciever")
        message= form.getvalue("message")

        # Grab Table values
    
        add_message = """
        INSERT INTO
            users (message, sender, reciever)
        VALUES
        ('"""+message+"""','"""+sender+"""','"""+reciever+"""');
        """

        execute_query(connection, add_message)

        selected_users = "SELECT * from users"
        users = execute_read_query(connection, selected_users)

        print(users)

        self.wfile.write("<html><body><h1>POST Request Received!</h1></body></html>")

def run(server_class=HTTPServer, handler_class=GP, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Server running at localhost:80...'
    httpd.serve_forever()

run()

