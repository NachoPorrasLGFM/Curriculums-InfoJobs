import os
import subprocess
from tkinter import Tk, Label, Entry, Button, filedialog, messagebox
from PyPDF2 import PdfReader, PdfWriter
from pdfminer.high_level import extract_text

def split_pdf_by_keyword(input_pdf, keyword):
    # Crear carpeta de salida si no existe
    output_folder = "./split_pdfs"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Leer el PDF de entrada
    input_pdf_reader = PdfReader(open(input_pdf, "rb"))
    
    # Inicializar variables
    pdf_writer = PdfWriter()
    part_num = 1
    start_new_pdf = False
    
    for page_num in range(len(input_pdf_reader.pages)):
        # Extraer texto de la página actual
        page_text = extract_text(input_pdf, page_numbers=[page_num])
        
        # Verificar si la página contiene la palabra clave
        if keyword in page_text:
            if start_new_pdf:
                # Guardar el PDF actual y resetear el escritor de PDF
                output_pdf_path = os.path.join(output_folder, f"part_{part_num}.pdf")
                with open(output_pdf_path, "wb") as output_pdf_file:
                    pdf_writer.write(output_pdf_file)
                pdf_writer = PdfWriter()  # Resetear el escritor de PDF
                part_num += 1
            start_new_pdf = True
        
        # Agregar página al escritor de PDF
        pdf_writer.add_page(input_pdf_reader.pages[page_num])
    
    # Guardar el último PDF si tiene páginas
    if len(pdf_writer.pages) > 0:
        output_pdf_path = os.path.join(output_folder, f"part_{part_num}.pdf")
        with open(output_pdf_path, "wb") as output_pdf_file:
            pdf_writer.write(output_pdf_file)

    # Mostrar mensaje de éxito
    messagebox.showinfo("Éxito", f"El PDF ha sido dividido en {part_num} partes.")

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        entry_input_pdf.delete(0, "end")
        entry_input_pdf.insert(0, file_path)

def start_splitting():
    input_pdf = entry_input_pdf.get()
    keyword = entry_keyword.get()
    if input_pdf and keyword:
        split_pdf_by_keyword(input_pdf, keyword)
    else:
        messagebox.showwarning("Advertencia", "Por favor, ingrese todos los campos.")

def open_output_folder():
    output_folder = "./split_pdfs"
    if os.path.exists(output_folder):
        # Abrir la carpeta en el explorador de archivos
        if os.name == 'nt':  # Windows
            os.startfile(output_folder)
        elif os.name == 'posix':  # macOS, Linux
            subprocess.call(['open', output_folder] if os.uname().sysname == 'Darwin' else ['xdg-open', output_folder])
    else:
        messagebox.showwarning("Advertencia", "La carpeta de salida no existe.")

# Crear la ventana principal
root = Tk()
root.title("Divisor de PDF por Palabra Clave")

# Crear y ubicar los elementos de la interfaz gráfica
Label(root, text="Archivo PDF de entrada:").grid(row=0, column=0, padx=10, pady=10)
entry_input_pdf = Entry(root, width=50)
entry_input_pdf.grid(row=0, column=1, padx=10, pady=10)
Button(root, text="Seleccionar archivo", command=select_file).grid(row=0, column=2, padx=10, pady=10)

Label(root, text="Palabra clave:").grid(row=1, column=0, padx=10, pady=10)
entry_keyword = Entry(root, width=50)
entry_keyword.insert(0, "Por leer en")  # Palabra clave por defecto
entry_keyword.grid(row=1, column=1, padx=10, pady=10)

Button(root, text="Dividir PDF", command=start_splitting).grid(row=2, column=0, columnspan=2, pady=20)

# Iniciar el bucle principal de la interfaz gráfica
root.mainloop()