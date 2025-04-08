import tkinter as tk
import threading
import socket
import queue

class App:
    def __init__(self, master):
        self.master = master
        master.title("Socket Reader")

        self.label_text = tk.StringVar()
        self.label = tk.Label(master, textvariable = self.label_text)
        self.label.pack()

        self.entry = tk.Entry(master)
        self.entry.pack()

        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.pack()

        self.sock = None

        self.data_queue = queue.Queue()
        self.running = True

        self.socket_thread = threading.Thread(target=self.read_socket)
        self.socket_thread.daemon = True  # Allow program to exit even if thread is running
        self.socket_thread.start()

        self.update_gui()

    def send_message(self):
        if self.sock:
            message = self.entry.get()
            self.sock.send(message.encode())
            self.entry.delete(0, tk.END)

    def read_socket(self):
        host = "localhost"  # Or "localhost"
        port = 801        # Replace with your port

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, port))
            while self.running:
                data = self.sock.recv(1024)
                if not data:
                    break
                self.data_queue.put(data.decode())
        except Exception as e:
             self.data_queue.put(f"Error: {e}")

    def update_gui(self):
        try:
            data = self.data_queue.get_nowait()
            self.label_text.set(data)
        except queue.Empty:
            pass  # No data yet, ignore
        if self.running:
            self.master.after(100, self.update_gui) # Check every 100 ms
        

    def close(self):
        self.running = False
        self.master.destroy()


root = tk.Tk()
app = App(root)
root.protocol("WM_DELETE_WINDOW", app.close) # Handle window close event
root.mainloop()