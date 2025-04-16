import unittest
from client_release import PollClient
from server_release import PollServer
from main import Chatroom, start_client, start_server
import os


class TestChatroom(unittest.TestCase):
    def test_basic_set_up(self):
        app = Chatroom()
        with open("chatroom_info.txt", "w") as f:
                self.username = "Test_Username"
                self.IP = "127.0.0.1"
                self.Port = "53827"
        with open("chatroom_text.txt", "w") as f: 
                self.chatroom_text = "Test Chat Message"
        
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
        
    def test_w_clear_info(self):
        os.remove("chatroom_info.txt")
        os.remove("chatroom_text.txt")
        app = Chatroom()
        
    def test_send_message(self):
        app = Chatroom()
        start_client(app, '127.0.0.1', 53827, 'Test_Username')
        app.frames["Chatroom_Page"].curr_message.set("Test Message")
        app.frames["Chatroom_Page"].send_message()

    def test_update_chat_box(self):
        app = Chatroom()
        start_client(app, '127.0.0.1', 53827, 'Test_Username')
        text = "This is a test."
        sender = "Test_username"

        app.frames["Chatroom_Page"].update_chat_box(text, sender)

    def test_clear_chat(self):
        app = Chatroom()
        start_client(app, '127.0.0.1', 53827, 'Test_Username')
        app.frames["Chatroom_Page"].clear_chat()


if __name__ == "__main__":
    unittest.main()
