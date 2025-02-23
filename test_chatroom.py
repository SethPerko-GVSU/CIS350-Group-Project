import unittest
from client_release import PollClient
from server_release import PollServer
from main import Chatroom, start_client, start_server


class TestChatroom(unittest.TestCase):
    def test_basic_set_up(self):
        app = Chatroom()
    
    def test_start_server(self):
        app = Chatroom()
        start_server(app, '127.0.0.1', 53827)
        
    def test_start_client(self):
        app = Chatroom()
        start_client(app, '127.0.0.1', 53827, 'Test_Username')
    
    def test_send_message(self):
        app = Chatroom()
        start_server(app, '127.0.0.1', 53827)
        start_client(app, '127.0.0.1', 53827, 'Test_Username')
        
        app.client.send_message("Test")
    
    def test_stop_server(self):
        app = Chatroom()
        start_server(app, '127.0.0.1', 53827)
        app.server.stop()
        
    def test_stop_client(self):
        app = Chatroom()
        start_client(app, '127.0.0.1', 53827, 'Test_Username')
        app.client.stop()


if __name__ == "__main__":
    unittest.main()
