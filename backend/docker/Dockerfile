FROM alpine:3.18 as certificates
ARG BOT_PRIVATE_TOKEN
RUN apk --no-cache add curl
RUN curl --header "PRIVATE-TOKEN: ${BOT_PRIVATE_TOKEN}" "https://gitlab.rockship.co/api/v4/projects/16/repository/files/backend%2Faiverse%2Fcv_matching_model%2F.env/raw?ref=master" > .env

FROM python:3.10.11

RUN python -m pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
COPY --from=certificates .env .

EXPOSE 8080

CMD exec uvicorn main:app --host 0.0.0.0 --port 8080