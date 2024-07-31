FROM python:3.11

RUN git config --global core.filemode false && \
    git config --global core.autocrlf true && \
    pip install --upgrade pip

CMD ["tail", "-f", "/dev/null"]
    