import os
import re

# Directorio raíz del blog
blog_root = '../filosofia-politica'  # Ajusta esta ruta según tu estructura 'ruta/a/tu/carpeta/de/blog'

# Iterar sobre todas las carpetas en el directorio del blog (subblogs)
for subblog in os.listdir(blog_root):
    subblog_path = os.path.join(blog_root, subblog)
    if os.path.isdir(subblog_path):
        # Eliminar números del nombre de la carpeta subblog
        subblog_name = re.sub(r'\d+', '', subblog)
        subblog_name = subblog_name.replace('-', ' ')

        # Convertir el nombre a mayúsculas y minúsculas
        subblog_name = subblog_name.title()

        # Iterar sobre todas las carpetas dentro de cada subblog
        for folder in os.listdir(subblog_path):
            folder_path = os.path.join(subblog_path, folder)
            if os.path.isdir(folder_path):
                # Construir la ruta completa al archivo index.qmd
                qmd_file = os.path.join(folder_path, 'index.qmd')

                if os.path.exists(qmd_file):
                    # Leer el contenido del archivo .qmd
                    with open(qmd_file, 'r', encoding='utf-8') as file:
                        content = file.read()

                    # Actualizar las categorías
                    updated_content = re.sub(r'categories:\n\s*-.*', f'categories:\n  - {subblog_name}', content, count=1)

                    # Escribir el contenido actualizado de vuelta al archivo
                    with open(qmd_file, 'w', encoding='utf-8') as file:
                        file.write(updated_content)
                else:
                    print(f"No se encontró index.qmd en {folder_path}")
