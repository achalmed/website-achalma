#!/bin/bash

# Nombre del blog principal (como "blog"), ahora relativo a la carpeta script
main_blog="../macroeconomia"

# Función para convertir la ruta a un enlace Markdown con títulos más legibles
convert_to_link() {
    local path="$1"
    local folder_name=$(basename "$path")
    # Sacar la fecha y convertir guiones en espacios
    local title=$(echo "$folder_name" | sed 's/^[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}-//' | tr '-' ' ' | sed 's/\b\(.\)/\u\1/g')
    local subblog=$(dirname "$path" | xargs basename)
    # Usar una ruta absoluta para la URL sin añadir ../
    local url="https://achalmaedison.netlify.app/$subblog/$folder_name"
    local pdf_url="$url/index.pdf"

    echo -e "[$title]($url) Lee sin conexión 📚 [PDF]($pdf_url)"
}

# Procesar cada subblog dentro del main_blog
for subblog in "$main_blog"/*; do
    if [ -d "$subblog" ]; then
        # Nombre del archivo de salida para cada subblog
        output_file="$subblog/_contenido_${subblog##*/}.qmd"

        # Crear o limpiar el archivo de salida
        > "$output_file"

        # Enumerar y procesar cada carpeta con fecha dentro del subblog
        count=1
        for dated_folder in "$subblog"/*; do
            if [ -d "$dated_folder" ]; then
                echo -e "$count. $(convert_to_link "$dated_folder")" >> "$output_file"
                ((count++))
            fi
        done

        echo "Archivo generado: $output_file"
    fi
done

echo "Proceso completado."
