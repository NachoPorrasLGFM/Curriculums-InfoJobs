import os
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

# Ejemplo de uso
split_pdf_by_keyword("./InfoJobs - CV.pdf", "Por leer en")

# Listar los archivos generados
output_folder = "./split_pdfs"
os.listdir(output_folder)
