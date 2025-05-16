#!/bin/bash

# Nombre del blog principal (cambia esto a la carpeta que desees procesar)
main_blog="../gestion-empresarial"  # Por ejemplo, cambia a "../finanzas" o "../macroeconomia" según sea necesario

# Función para convertir la ruta a un enlace Markdown con títulos más legibles
convert_to_link() {
    local path="$1"
    local folder_name=$(basename "$path")
    # Sacar la fecha y convertir guiones en espacios
    local title=$(echo "$folder_name" | sed 's/^[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}-//' | tr '-' ' ' | sed 's/\b\(.\)/\u\1/g')
    local subblog=$(dirname "$path" | xargs basename)
    # Obtener el nombre de la carpeta principal (sin "../")
    local main_folder=$(basename "$main_blog")
    # Ajustar la URL para usar el nombre de la carpeta principal correcta
    local url="https://achalmaedison.netlify.app/$main_folder/$subblog/$folder_name"
    local pdf_url="$url/index.pdf"

    echo -e "[{{< fa regular file-pdf >}}]($pdf_url) [$title]($url)"
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
