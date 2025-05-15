import os
import argparse
import hashlib
from pathlib import Path

# Instrucciones de uso: python create_hardlinks.py _contenido-inicio.qmd o python create_hardlinks.py documento.py --exclude temp

# Lista de carpetas a excluir (puedes añadir más aquí)
EXCLUDED_DIRS = [
    "_extensions",
    "_freeze",
    "_partials",
    ".idea",
    ".github",
    ".obsidian",
    ".git",
    ".vscode",
    ".quarto",
    "_site",
    # Añade más carpetas aquí si es necesario, por ejemplo:
    # "node_modules",
    # "dist",
]

def calculate_file_hash(filepath):
    """Calcula el hash SHA-256 de un archivo."""
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            # Leer el archivo en fragmentos para manejar archivos grandes
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except OSError as e:
        print(f"Error al calcular hash para {filepath}: {e}")
        return None

def get_inode(filepath):
    """Obtiene el número de inodo de un archivo."""
    try:
        return os.stat(filepath).st_ino
    except OSError as e:
        print(f"Error al obtener inodo para {filepath}: {e}")
        return None

def create_hardlinks(search_dir, filename, exclude_dirs):
    """
    Busca archivos con nombre exacto recursivamente y reemplaza los encontrados con hard links
    al primer archivo encontrado (fuente principal), si los hash coinciden y los inodos difieren.
    Excluye las carpetas especificadas.
    """
    # Normalizar la lista de carpetas excluidas para comparación
    exclude_dirs = set(os.path.normpath(os.path.join(search_dir, d)) for d in exclude_dirs)
    
    # Variable para almacenar el archivo fuente principal
    source_path = None
    source_hash = None
    source_inode = None
    
    # Recorrer recursivamente el directorio de búsqueda
    for root, dirs, files in os.walk(search_dir, topdown=True):
        # Excluir directorios especificados
        dirs[:] = [d for d in dirs if os.path.normpath(os.path.join(root, d)) not in exclude_dirs]
        
        # Buscar archivos que coincidan exactamente con el nombre
        if filename in files:
            current_path = os.path.join(root, filename)
            
            try:
                # Si no tenemos un archivo fuente principal, usar el primero encontrado
                if source_path is None:
                    source_path = current_path
                    source_hash = calculate_file_hash(source_path)
                    source_inode = get_inode(source_path)
                    if source_hash is None or source_inode is None:
                        print(f"No se puede usar {source_path} como fuente principal: Error al obtener hash o inodo.")
                        return
                    print(f"Archivo fuente principal: {source_path}")
                    continue
                
                # Verificar inodo y hash del archivo actual
                current_inode = get_inode(current_path)
                if current_inode is None:
                    print(f"No se puede procesar {current_path}: Error al obtener inodo.")
                    continue
                
                # Si tienen el mismo inodo, ya es un hard link
                if current_inode == source_inode:
                    print(f"Omitiendo {current_path}: Ya es un hard link del archivo fuente (mismo inodo).")
                    continue
                
                # Comparar hash para verificar si el contenido es idéntico
                current_hash = calculate_file_hash(current_path)
                if current_hash is None:
                    print(f"No se puede procesar {current_path}: Error al calcular hash.")
                    continue
                
                if current_hash != source_hash:
                    print(f"Advertencia: {current_path} tiene contenido diferente (hash no coincide), omitiendo reemplazo.")
                    continue
                
                # Reemplazar el archivo actual con un hard link al archivo fuente
                os.remove(current_path)
                os.link(source_path, current_path)
                print(f"Hard link creado: {current_path} -> {source_path}")
            
            except OSError as e:
                print(f"Error al crear hard link para {current_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Busca archivos por nombre exacto y reemplaza con hard links al primer archivo encontrado.")
    parser.add_argument("filename", help="Nombre exacto del archivo a buscar (ej. '_contenido-final.qmd', 'documento.py')")
    parser.add_argument("--exclude", nargs="*", default=EXCLUDED_DIRS, 
                       help="Carpetas a excluir (adicionales a las predefinidas)")
    
    args = parser.parse_args()
    
    # Directorio superior (un nivel arriba del script)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    search_dir = os.path.abspath(os.path.join(script_dir, ".."))
    
    print(f"Buscando archivo '{args.filename}' en {search_dir}")
    if args.exclude:
        print(f"Excluyendo carpetas: {', '.join(args.exclude)}")
    
    create_hardlinks(search_dir, args.filename, args.exclude)

if __name__ == "__main__":
    main()