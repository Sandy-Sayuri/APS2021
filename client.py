
from tkinter import Message, font
from tkinter.constants import SEL_FIRST
import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

HOST = '127.0.0.1'
PORT = 9090

class Client:
    def __init__(self, host, port):
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        msg = tkinter.Tk()
        msg.withdraw()

        self.nickname = simpledialog.askstring("Usuario", "nome do usuario",parent = msg)

        self.gui_done = False

        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)

        gui_thread.start()
        receive_thread.start()

    def gui_loop(self):
        self.win = tkinter.Tk("Usuario")
        self.win.config(padx=10,pady=10,bg="lightgray")
        self.chat_label = tkinter.Label(self.win, text="chat: ", bg="lightgray")
        self.chat_label.config(font=("Arial",12))
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state='disabled')

        self.msg_label = tkinter.Label(self.win, text="mensegem: ", bg="lightgray")
        self.msg_label.config(font=("Arial",12))
        self.msg_label.pack(padx=20, pady=5)

        self.input_area = tkinter.Text(self.win, height=3)
        self.input_area.pack(padx=20, pady=5)
#botão de mandar 
        self.send_button =tkinter.Button(self.win, text="enviar", command=self.write)
        self.send_button.config(font=("Arial", 12))
        self.send_button.pack(padx=500, pady=5)
#emojis
        self.send_button =tkinter.Button(self.win, width=10, text="(^o^)", command=self.feliz,)
        self.send_button.config(font=("Arial", 12))
        self.send_button.pack(padx=20, pady=5)
        self.send_button =tkinter.Button(self.win, text="(^o^;", command=self.triste)
        self.send_button.config(font=("Arial", 12))
        self.send_button.pack(padx=20, pady=5)
        self.send_button =tkinter.Button(self.win, text="(-- _ --)", command=self.tanto_faz)
        self.send_button.config(font=("Arial", 12))
        self.send_button.pack(padx=20, pady=5)
        self.send_button =tkinter.Button(self.win, text="(*^_^*)", command=self.fofo)
        self.send_button.config(font=("Arial", 12))
        self.send_button.pack(padx=20, pady=5)

        self.gui_done = True
        self.win.protocol("WM_DELETE_WINDOW",self.stop)

        self.win.mainloop()
#função emosji fofo
    def fofo(self):
        message = (f"{self.nickname}:(*^_^*)\n")
        self.sock.send(message.encode('UTF-8'))
        self.input_area.delete('1.0', 'end')        
#função emosji tanto_faz
    def tanto_faz(self):
        message = (f"{self.nickname}:(-- _ -- )\n")
        self.sock.send(message.encode('UTF-8'))
        self.input_area.delete('1.0', 'end')
#função emosji triste
    def triste(self):
        message = (f"{self.nickname}:(^o^;\n")
        self.sock.send(message.encode('UTF-8'))
        self.input_area.delete('1.0', 'end')
#função emosji feliz
    def feliz(self):
        message = (f"{self.nickname}:(^o^)\n")
        self.sock.send(message.encode('UTF-8'))
        self.input_area.delete('1.0', 'end')
        

    def write(self):
        message = (f"{self.nickname}: {self.input_area.get('1.0', 'end')}")
        self.sock.send(message.encode('UTF-8'))
        self.input_area.delete('1.0', 'end')

    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024)
                if message == 'NICK':
                    self.sock.send(self.nickname.encode('utf-8'))
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')   
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')
            except ConnectionAbortedError:
                print("ERROR 1")
                break
            except:
                print("ERROR 2")
                self.sock.close()
                break
            
client = Client(HOST,PORT)