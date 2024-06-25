FROM python:3.11

COPY . /openfisca
WORKDIR /openfisca

RUN pip install --upgrade pip && \
    pip install --upgrade .

EXPOSE 5000

CMD [ "/usr/local/bin/openfisca", "serve", "-b", "0.0.0.0:5000" ]
