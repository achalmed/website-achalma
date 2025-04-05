import xml.etree.ElementTree as ET
import os

# Lista de rutas a los archivos RSS individuales dentro de _site
feeds = [
    '../_site/blog/index.xml', # Agrega más según tus carpetas
    '../_site/finanzas/index.xml',
    '../_site/econometria/index.xml',
    '../_site/filosofia-politica/index.xml',
    '../_site/gestion-publica-herramientas/index.xml',  
    '../_site/herramientas-oficina/index.xml',
    '../_site/investigacion-metodologia/index.xml',
    '../_site/macroeconomia/index.xml',
    '../_site/matematicas/index.xml',
    '../_site/microeconomia/index.xml',
    '../_site/programacion-software/index.xml',
    '../_site/teching/index.xml',
    '../_site/tecnologia-seguridad/index.xml',
]

# Crear el nuevo documento RSS
rss = ET.Element("rss", version="2.0")
channel = ET.SubElement(rss, "channel")
ET.SubElement(channel, "title").text = "Feed General - Todos los Blogs"
ET.SubElement(channel, "link").text = "https://achalmaedison.netlify.app/"  # Cambia por tu dominio real
ET.SubElement(channel, "description").text = "Feed consolidado de todos los blogs"

# Combinar items de cada feed
for feed_file in feeds:
    if os.path.exists(feed_file):  # Verifica que el archivo exista
        tree = ET.parse(feed_file)
        root = tree.getroot()
        for item in root.find("channel").findall("item"):
            channel.append(item)
    else:
        print(f"Advertencia: No se encontró el archivo {feed_file}")

# Guardar el archivo index.xml
tree = ET.ElementTree(rss)
tree.write("../_site/index.xml", encoding="utf-8", xml_declaration=True)  # Guarda en _site/
