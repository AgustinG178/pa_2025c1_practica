import matplotlib
matplotlib.use('Agg')  # Configura un backend no interactivo
import matplotlib.pyplot as plt
import os
from collections import defaultdict
from matplotlib.backends.backend_pdf import PdfPages
def graficar_intentos_vs_aciertos(file_path, output_folder):
    """
    Genera un gráfico de torta con los aciertos y errores totales.
    Args:
        file_path (str): Ruta al archivo de resultados.
        output_folder (str): Carpeta donde se guardará el gráfico.
    """
    aciertos_totales = 0
    intentos_totales = 0
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip() and "Usuario:" in line and "Resultado:" in line:
                parts = line.strip().split(" / ")
                try:
                    resultado = parts[1].split(":")[1]
                    correctos, total = map(int, resultado.split("/"))
                    aciertos_totales += correctos
                    intentos_totales += total
                except (IndexError, ValueError):
                    print(f"Línea con formato incorrecto: {line.strip()}")
                    continue
    labels = ['Aciertos', 'Errores']
    sizes = [aciertos_totales, intentos_totales - aciertos_totales]
    colors = ['skyblue', 'lightcoral']
    explode = (0.1, 0)
    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors, explode=explode)
    plt.title('Resultados Generales')
    plt.axis('equal')
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, "grafico_torta_general.png")
    plt.savefig(output_path)
    plt.close()

def graficar_aciertos_vs_desaciertos_por_fecha(file_path, output_folder):
    """
    Genera un gráfico con dos curvas: una para los aciertos y otra para los desaciertos,
    en función de las fechas de juego para todos los usuarios.
    Args:
        file_path (str): Ruta al archivo de resultados.
        output_folder (str): Carpeta donde se guardará el gráfico.
    """
    fechas = defaultdict(lambda: {"aciertos": 0, "desaciertos": 0})
    with open(file_path, 'r', encoding="utf-8") as file:
        for line in file:
            if line.strip() and "Usuario:" in line and "Resultado:" in line:
                parts = line.strip().split(" / ")
                try:
                    fecha = parts[2].split(":")[1].strip()
                    resultado = parts[1].split(":")[1]
                    aciertos, total = map(int, resultado.split("/"))
                    desaciertos = total - aciertos
                    fechas[fecha]["aciertos"] += aciertos
                    fechas[fecha]["desaciertos"] += desaciertos
                except (IndexError, ValueError):
                    print(f"Línea con formato incorrecto: {line.strip()}")
                    continue
    fechas_ordenadas = sorted(fechas.items())
    fechas_labels = [fecha for fecha, _ in fechas_ordenadas]
    aciertos_totales = [data["aciertos"] for _, data in fechas_ordenadas]
    desaciertos_totales = [data["desaciertos"] for _, data in fechas_ordenadas]
    plt.figure(figsize=(10, 6))
    plt.plot(fechas_labels, aciertos_totales, label="Aciertos", marker="o", color="green")
    plt.plot(fechas_labels, desaciertos_totales, label="Desaciertos", marker="o", color="red")
    plt.xlabel("Fechas")
    plt.ylabel("Cantidad")
    plt.title("Aciertos vs Desaciertos por Fecha")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, "grafico_curvas_aciertos_desaciertos.png")
    plt.savefig(output_path)
    plt.close()

def convertir_pdf(filename):
    """
    Convierte una imagen PNG a un archivo PDF.
    Args:
        filename (str): Nombre del archivo PNG que se desea convertir. 
                        Debe estar ubicado en la carpeta "static/graficos".
    Returns:
        str: Ruta al archivo PDF generado.
    Raises:
        FileNotFoundError: Si el archivo PNG no se encuentra en la ruta especificada.
    Nota:
        La función utiliza Matplotlib para leer la imagen PNG y guardarla como un PDF.
        El archivo PDF se guarda en la misma carpeta que el archivo PNG original.
    """
    ""
    # Ruta al archivo PNG
    image_path = os.path.join("static/graficos", filename)
    
    # Ruta para guardar el archivo PDF temporal
    pdf_path = os.path.join("static/graficos", f"{os.path.splitext(filename)[0]}.pdf")
    
    # Convertir la imagen PNG a PDF
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"El archivo de imagen no se encontró en la ruta: {image_path}")
    img = plt.imread(image_path)
    plt.figure(figsize=(8, 6))
    plt.imshow(img)
    plt.axis('off')  # Ocultar los ejes
    with PdfPages(pdf_path) as pdf:
        pdf.savefig()  # Guardar la figura en el PDF
    plt.close()

    return pdf_path

if __name__ == "__main__":
    # Ejemplo de uso de las funciones
    graficar_intentos_vs_aciertos("data/resultados.txt", "static/graficos")
    graficar_aciertos_vs_desaciertos_por_fecha("data/resultados.txt", "static/graficos")
    convertir_pdf("grafico_torta_general.png")