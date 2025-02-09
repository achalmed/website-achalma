import os
import re

# Directorio raíz del blog
blog_root = '../blog'  # Ajusta esta ruta según tu estructura 'ruta/a/tu/carpeta/de/blog'

# Iterar sobre todas las carpetas en el directorio del blog (subblogs)
for subblog in os.listdir(blog_root):
    subblog_path = os.path.join(blog_root, subblog)
    if os.path.isdir(subblog_path):
        # Iterar sobre todas las carpetas dentro de cada subblog
        for folder in os.listdir(subblog_path):
            folder_path = os.path.join(subblog_path, folder)
            if os.path.isdir(folder_path):
                # Extraer la fecha del nombre de la carpeta en formato año-mes-día
                match = re.match(r'(\d{4})-(\d{2})-(\d{2})', folder)
                if match:
                    year, month, day = match.groups()
                    # Convertir a formato mes/día/año
                    date_from_folder = f"{month}/{day}/{year}"

                    # Construir la ruta completa al archivo index.qmd
                    qmd_file = os.path.join(folder_path, 'index.qmd')

                    if os.path.exists(qmd_file):
                        # Leer el contenido del archivo .qmd
                        with open(qmd_file, 'r', encoding='utf-8') as file:
                            content = file.read()

                        # Actualizar el enlace del PDF en la descripción
                        blog_name = os.path.basename(blog_root)
                        updated_content = re.sub(r'\(https:\/\/achalmaedison\.netlify\.app\/.*\/index\.pdf\)', f'(https://achalmaedison.netlify.app/{blog_name}/{subblog}/{folder}/index.pdf)', content)

                        # Actualizar el enlace del PDF en la citación
                        updated_content = re.sub(r'citation:\n  pdf-url: .*', f'citation:\n  pdf-url: https://achalmaedison.netlify.app/{blog_name}/{subblog}/{folder}/index.pdf', updated_content)

                        # Escribir el contenido actualizado de vuelta al archivo
                        with open(qmd_file, 'w', encoding='utf-8') as file:
                            file.write(updated_content)
                    else:
                        print(f"No se encontró index.qmd en {folder_path}")
                else:
                    print(f"La carpeta {folder} no tiene una fecha en su nombre en el formato esperado.")

print("Actualización de enlaces del PDF completada.")
