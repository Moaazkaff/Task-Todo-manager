FROM python:3.14-alpine3.24

RUN addgroup -S -g 1001 pythongroup && \
    adduser -S -u 1001 -G pythongroup pythonuser

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=pythonuser:pythongroup . .

EXPOSE 5000

USER pythonuser

ENTRYPOINT [ "python" , "app.py" ]


