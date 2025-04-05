import xml.etree.ElementTree as ET
import os
from datetime import datetime
import datetime as dt  # Importa el módulo completo para usar datetime.UTC

# Lista de rutas a los archivos RSS individuales dentro de _site
feeds = [
    '../_site/blog/index.xml',
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

# Crear el nuevo documento RSS con namespaces
rss = ET.Element("rss", {
    "version": "2.0",
    "xmlns:atom": "http://www.w3.org/2005/Atom",
    "xmlns:dc": "http://purl.org/dc/elements/1.1/",
    "xmlns:media": "http://search.yahoo.com/mrss/",
    "xmlns:content": "http://purl.org/rss/1.0/modules/content/"
})
channel = ET.SubElement(rss, "channel")
ET.SubElement(channel, "title").text = "Achalma Edison - Todos los Blogs"
ET.SubElement(channel, "link").text = "https://achalmaedison.netlify.app/"
ET.SubElement(channel, "description").text = "Feed consolidado de todos los blogs"
ET.SubElement(channel, "atom:link", {
    "href": "https://achalmaedison.netlify.app/index.xml",
    "rel": "self",
    "type": "application/rss+xml"
})
ET.SubElement(channel, "generator").text = "Python RSS Combiner"
ET.SubElement(channel, "lastBuildDate").text = datetime.now(dt.UTC).strftime("%a, %d %b %Y %H:%M:%S GMT")

# Combinar items de cada feed
for feed_file in feeds:
    if os.path.exists(feed_file):
        tree = ET.parse(feed_file)
        root = tree.getroot()
        for item in root.find("channel").findall("item"):
            channel.append(item)  # Copia el item completo, incluyendo CDATA si lo tiene
    else:
        print(f"Advertencia: No se encontró el archivo {feed_file}")

# Guardar el archivo index.xml
tree = ET.ElementTree(rss)
tree.write("../_site/index.xml", encoding="utf-8", xml_declaration=True)

