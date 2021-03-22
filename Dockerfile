# Create builder
FROM python:3.8.0-slim as builder
RUN apt-get update \
&& apt-get install gcc -y \
&& apt-get clean
COPY requirement.txt /app/requirement.txt
WORKDIR app
RUN pip install --user -r requirement.txt

COPY ./server.py /app
COPY ./internal /app/internal

# Main Image
FROM python:3.8.0-slim as app
COPY --from=builder /root/.local /root/.local
COPY --from=builder /app /app
WORKDIR /app
ENV PATH=/root/.local/bin:$PATH

# expose port 3001 on the vm
EXPOSE 3001

# run `npm start` to setup the server
CMD [ "python", "server.py" ]
