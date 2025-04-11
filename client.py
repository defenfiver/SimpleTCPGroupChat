import tkinter as tk
from tkinter import ttk, simpledialog
import threading
import socket
import queue
import tkinter
import tkinter.dialog
import tkinter.messagebox
import tkinter.simpledialog

class App:
    def __init__(self, master):
        self.master = master
        master.title("Socket Reader")
        master.geometry("500x400")

        # prompt for user name
        self.name = simpledialog.askstring("Name", "Enter your name:")
        if not self.name:
            master.destroy()
            master.quit()
            return
        global nameHappened
        nameHappened = True

        self.top_frame = tk.Frame(master)
        self.top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.top_frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.top_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.LEFT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.messages_frame = tk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0,0), window=self.messages_frame, anchor="nw")

        self.messages_frame.bind("<Configure>", self.on_frame_configure)

        self.bottom_frame = tk.Frame(master)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.entry = tk.Entry(self.bottom_frame)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)

        self.send_button = tk.Button(
            self.bottom_frame, text="Send", command=self.send_message
        )
        self.send_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.sock = None
        self.data_queue = queue.Queue()
        self.running = True

        self.socket_thread = threading.Thread(target=self.read_socket, daemon=True)
        self.socket_thread.start()

        self.update_gui()

    def send_name(self):
        if self.sock:
            self.sock.send(self.name.encode())

    def send_message(self):
        if self.sock:
            message = self.entry.get()
            self.sock.send(message.encode())
            self.entry.delete(0, tk.END)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def show_message(self, text):
        label = tk.Label(
            self.messages_frame,
            text=text,
            anchor="w",
            justify="left",
            wraplength=400
        )
        label.pack(fill=tk.X, expand=True, padx=5, pady=5)

        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1.0)

    def read_socket(self):
        host = "localhost"  # Or "localhost"
        port = 5001

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, port))
            self.send_name()
            while self.running:
                data = self.sock.recv(1024)
                if not data:
                    break
                self.data_queue.put(data.decode())
        except ConnectionResetError:
            app.close()
            errorHappened = True
            return
        except Exception as e:
             self.data_queue.put(f"Error: {e}")

    def update_gui(self):
        try:
            while self.running:
                msg = self.data_queue.get_nowait()
                self.show_message(msg)
            app.close()
            return
        except queue.Empty:
            pass

        if self.running:
            self.master.after(100, self.update_gui)

    def safeclose(self):
        self.running = False
        if self.sock:
            self.sock.close()
        # self.master.destroy()
        self.master.quit()

    def close(self):
        self.safeclose()
        tmp = tk.Tk()
        tkinter.messagebox.showerror("Error", "Server closed unexpectedly")

errorHappened = False
global nameHappened
nameHappened = False
root = tk.Tk()
app = App(root)
root.protocol("WM_DELETE_WINDOW", app.safeclose) # Handle window close event
if nameHappened:
    root.mainloop()

