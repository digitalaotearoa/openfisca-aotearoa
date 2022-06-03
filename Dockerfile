FROM python:3.10

COPY . /openfisca
WORKDIR /openfisca

RUN pip install --upgrade pip && \
    pip install . --use-deprecated=legacy-resolver

EXPOSE 5000

CMD [ "/usr/local/bin/openfisca", "serve", "-b", "0.0.0.0:5000" ]
