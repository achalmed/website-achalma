# api/Dockerfile — imagen de la API del aula (perfil «api» del compose); los datos se montan en /datos.
FROM python:3.13-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY aula ./aula
RUN useradd --create-home --uid 1000 aula && mkdir -p /datos && chown aula /datos
USER aula
EXPOSE 8040
CMD ["uvicorn", "aula.main:app", "--host", "0.0.0.0", "--port", "8040", "--proxy-headers", "--no-access-log"]
