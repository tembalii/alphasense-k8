FROM python:3.11-slim
WORKDIR /app
COPY app.py /app/app.py
ENV CONFIG_PATH=/etc/myapp/config.yaml
ENV PORT=5000
EXPOSE 5000
CMD ["python", "app.py"]
