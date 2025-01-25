import tkinter as tk
from tkinter import ttk
import psutil
import time
class Network():
    def __init__(self,root):
    
     
        self.root=root
        self.root.title("Monitor de Tráfico de Red")# Titulo de l apk
        self.root.geometry("320x150")  # Tamaño inicial de la ventana
        self.root.iconbitmap("./img/wifi.ico")
        self.interface_label = ttk.Label(root, text="Interfaz de Red:")
        self.interface_label.pack(pady=5)
        self.interface_var = tk.StringVar()
        self.interfaces = list(psutil.net_io_counters(pernic=True).keys())
        self.interface_combobox = ttk.Combobox(root, textvariable=self.interface_var, values=self.interfaces, state="readonly")
        if self.interfaces:
            self.interface_combobox.current(0)
        self.interface_combobox.pack(pady=5)
        self.interface_combobox.bind("<<ComboboxSelected>>", self.update_interface)
        self.data_label = ttk.Label(root, text=f"Enviado: 0 KB/s\nRecibido: 0 KB/s")
        self.data_label.pack(pady=10)
        self.running = True
        self.root.protocol("WM_DELETE_WINDOW", self.stop) # Stop the monitor when the window is closed
        
        if self.interfaces:
            self.current_interface = self.interfaces[0]
            self.start_monitoring()
        else:
             self.data_label.config(text="No se detectaron interfaces de red.")
        


    def update_interface(self, event):
        self.current_interface = self.interface_var.get()
        self.start_monitoring

    def start_monitoring(self):
    
      self.running = True
      self.update()

    def stop(self):
        self.running = False
        self.root.destroy()
    
    def update(self):
        if not self.running:
             return
        counters_anterior = psutil.net_io_counters(pernic=True)
        wifi=counters_anterior[self.current_interface]
        bytes_enviados1=wifi.bytes_sent/1024
        bytes_recibidos1=wifi.bytes_recv/1024

        time.sleep(1)
        counters_actual=psutil.net_io_counters(pernic=True)
        wifi=counters_actual[self.current_interface]
        bytes_enviados2=wifi.bytes_sent/1024
        bytes_recibidos2=wifi.bytes_recv/1024
        bye=bytes_enviados2-bytes_enviados1
        byr=bytes_recibidos2-bytes_recibidos1
        text=f"Enviado: {bye:.2f} KB/s\nRecibido:{byr:.2f} KB/s"
        self.data_label.config(text=text)
        self.root.after(1000, self.update)
          
    
    
    
    
    
    
    
   

if __name__ == "__main__":
    root = tk.Tk()
    app = Network(root)
    root.mainloop()