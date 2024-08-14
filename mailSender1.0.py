import tkinter as tk
from tkinter import PhotoImage, messagebox
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Variables de configuración
sender = 'example@example.com'
password = 'pw'
server = 'smtp-es.securemail.pro'
port = 465


def on_button_click():
    # Obtener el texto de los cuadros de texto
    text1 = entry1.get("1.0", tk.END).strip()  # Lista de nombres
    template = entry2.get("1.0", tk.END).strip()  # Plantilla del correo

    # Obtener asunto y destinatario del formulario
    subject = subject_entry.get()
    recipient = recipient_entry.get()

    # Crear una nueva ventana de progreso
    progress_window = tk.Toplevel(root)
    progress_window.title("Enviando...")

    # Definir el tamaño de la ventana de progreso
    progress_window_width = 400
    progress_window_height = 150

    # Obtener el tamaño de la pantalla
    screen_width = progress_window.winfo_screenwidth()
    screen_height = progress_window.winfo_screenheight()

    # Calcular las coordenadas de la esquina superior izquierda
    x = (screen_width // 2) - (progress_window_width // 2)
    y = (screen_height // 2) - (progress_window_height // 2)

    # Establecer la geometría de la ventana de progreso
    progress_window.geometry(f"{progress_window_width}x{progress_window_height}+{x}+{y}")
    progress_window.configure(bg="#f0f0f0")  # Color de fondo de la ventana de progreso

    # Crear un spinner y un contador
    spinner = tk.Label(progress_window, text="Enviando...", anchor="center", font=("Helvetica", 14),
                       background="#FFFFFF")
    spinner.pack(pady=20, padx=20)
    counter_label = tk.Label(progress_window, text="Enviados: 0", anchor="center", font=("Helvetica", 14),
                             background="#FFFFFF")
    counter_label.pack(pady=10, padx=20)

    # Función para enviar correos
    def send_emails():
        lines = text1.splitlines()
        for i in range(len(lines)):  # Simular un proceso largo
            text_replaced = template.replace("{nombre}", lines[i])
            body = f"{text_replaced}"

            # Crear el mensaje
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = sender
            message["To"] = recipient

            part = MIMEText(body, "plain")
            message.attach(part)

            try:
                smtp_server = smtplib.SMTP_SSL(server, port)
                smtp_server.ehlo()
                smtp_server.login(sender, password)
                smtp_server.sendmail(sender, recipient, message.as_string())
                smtp_server.close()
            except Exception as ex:
                print("Ha ocurrido un error...", ex)

            spinner['text'] = f"Cargando{'.' * (i % 3 + 1)}"
            counter_label['text'] = f"Enviados: {i + 1}"
            progress_window.update_idletasks()  # Actualizar la interfaz para reflejar los cambios
            progress_window.after(250)  # Esperar 250 ms para simular el progreso

        messagebox.showinfo("Completado", "Proceso completado!")
        progress_window.destroy()  # Cerrar la ventana de progreso al finalizar

    # Iniciar la simulación del progreso
    send_emails()


# Crear la ventana principal
root = tk.Tk()
root.title("MailSender v1.0 by Samuel Aviles")

# Establecer el tamaño de la ventana principal
window_width = 600
window_height = 600

# Obtener el tamaño de la pantalla
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calcular las coordenadas de la esquina superior izquierda
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

# Establecer la geometría de la ventana principal
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Establecer el ícono de la ventana principal
icon = PhotoImage(file='icon.png')  # Reemplaza con la ruta a tu archivo .png
root.iconphoto(True, icon)

# Crear un marco (frame) para organizar los widgets
frame = tk.Frame(root, bg="#F0F0F0")
frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

# Crear los campos para asunto y destinatario
tk.Label(frame, text="Asunto del correo:", font=("Helvetica", 12)).grid(row=0, column=0, padx=20, pady=5, sticky="w")
subject_entry = tk.Entry(frame, width=30, font=("Helvetica", 12))
subject_entry.grid(row=0, column=1, padx=20, pady=5, sticky="e")
subject_entry.insert(0, "Asunto del correo")

tk.Label(frame, text="Destinatario:", font=("Helvetica", 12)).grid(row=1, column=0, padx=20, pady=5, sticky="w")
recipient_entry = tk.Entry(frame, width=30, font=("Helvetica", 12))
recipient_entry.grid(row=1, column=1, padx=20, pady=5, sticky="e")
recipient_entry.insert(0, "destinatario@ejemplo.com")

# Crear los cuadros de texto grandes
entry1 = tk.Text(frame, width=30, height=10, font=("Helvetica", 12), bd=2, relief="flat", bg="#FFFFFF", fg="#333333",
                 padx=10, pady=10)
entry1.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")
entry1.insert(tk.END, "Escriba la lista de nombres")

entry2 = tk.Text(frame, width=30, height=10, font=("Helvetica", 12), bd=2, relief="flat", bg="#FFFFFF", fg="#333333",
                 padx=10, pady=10)
entry2.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")
entry2.insert(tk.END, "Escriba el correo plantilla")

# Configurar las columnas y filas para que se expandan uniformemente
frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)
frame.rowconfigure(2, weight=1)  # Fila de los textos de entrada debe expandirse
frame.rowconfigure(3, weight=1)  # Fila de la plantilla debe expandirse

# Crear el botón
button = tk.Button(frame, text="Comenzar", command=on_button_click, font=("Helvetica", 14, "bold"), bg="#0DD8E6",
                   fg="black", padx=10, pady=10, relief="flat", borderwidth=2)
button.grid(row=4, column=0, columnspan=2, pady=20)

if __name__ == '__main__':
    # Ejecutar la aplicación
    root.mainloop()
