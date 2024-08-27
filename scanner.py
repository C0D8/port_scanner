import socket
import threading
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageSequence

# Função para escanear uma porta específica
def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            return True
        return False
    except Exception as e:
        print(f"Erro ao escanear a porta {port}: {e}")
        return False
    finally:
        sock.close()

# Função para obter o nome do serviço de uma porta
def get_service_name(port):
    try:
        service_name = socket.getservbyport(port)
        return service_name
    except OSError:
        return "Serviço desconhecido"

# Função para escanear portas em um intervalo
def scan_ports(ip, start_port, end_port, result_text):
    for port in range(start_port, end_port + 1):
        if scan_port(ip, port):
            service = get_service_name(port)
            result_text.insert(tk.END, f"Porta {port} ({service}) está aberta\n")
    messagebox.showinfo("Scan Completo", "O escaneamento foi concluído!")

# Função que é chamada ao clicar no botão de escaneamento
def start_scan():
    ip = ip_entry.get()
    start_port = int(start_port_entry.get())
    end_port = int(end_port_entry.get())
    
    result_text.delete(1.0, tk.END)
    scan_thread = threading.Thread(target=scan_ports, args=(ip, start_port, end_port, result_text))
    scan_thread.start()

# Função para redimensionar o gif de fundo e mantê-lo centralizado
def resize_and_center_gif(label, gif, window_width, window_height):
    frames = []
    for frame in ImageSequence.Iterator(gif):
        # Calcula as proporções do redimensionamento
        frame_width, frame_height = frame.size
        ratio = min(window_width / frame_width, window_height / frame_height)
        new_size = (int(frame_width * ratio), int(frame_height * ratio))
        resized_frame = frame.resize(new_size, Image.LANCZOS)
        frames.append(ImageTk.PhotoImage(resized_frame))
    
    def update_frame(ind):
        frame = frames[ind]
        ind = (ind + 1) % len(frames)
        label.config(image=frame)
        label.place(x=(window_width - frame.width()) // 2, y=(window_height - frame.height()) // 2)
        root.after(50, update_frame, ind)

    update_frame(0)

# Criação da interface gráfica
root = tk.Tk()
root.title("Scanner de Portas")

# Definindo o tamanho da janela como fullscreen
window_width = root.winfo_screenwidth()
window_height = root.winfo_screenheight()
root.geometry(f"{window_width}x{window_height}")

# Carrega o gif de fundo
gif = Image.open("back.gif")
background_label = tk.Label(root)
background_label.place(relwidth=1, relheight=1)  # Faz a imagem cobrir toda a janela
resize_and_center_gif(background_label, gif, window_width, window_height)  # Redimensiona e centraliza o gif

tk.Label(root, text="Endereço IP:").grid(row=0, column=0, padx=10, pady=10)
ip_entry = tk.Entry(root)
ip_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Porta Inicial:").grid(row=1, column=0, padx=10, pady=10)
start_port_entry = tk.Entry(root)
start_port_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Porta Final:").grid(row=2, column=0, padx=10, pady=10)
end_port_entry = tk.Entry(root)
end_port_entry.grid(row=2, column=1, padx=10, pady=10)

scan_button = tk.Button(root, text="Escanear", command=start_scan)
scan_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

result_text = tk.Text(root, height=15, width=50)
result_text.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
