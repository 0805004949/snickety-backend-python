FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1
LABEL maintainer 0805004949

# 220829, 0805004949, when using alpine setup the user
# FROM python:alpine3.15
# RUN addgroup app && adduser -SG app app
# USER app

WORKDIR /backend

# # shell prompt highlighting
RUN echo "alias egrep='egrep --color=auto'" >> ~/.basshrc && \
    echo "alias fgrep='fgrep --color=auto'" >> ~/.bashrc && \
    echo "alias grep='grep --color=auto'" >> ~/.bashrc  && \
    echo "alias l='ls -CF'" >> ~/.bashrc && \
    echo "alias la='ls -A'" >> ~/.bashrc && \
    echo "alias ll='ls -alF'" >> ~/.bashrc && \
    echo "alias ls='ls --color=auto'" >> ~/.bashrc

ENV FLASK_APP=app.py
ENV FLASK_DEBUG=1
EXPOSE 5000

COPY . /backend
RUN python -m pip install --upgrade pip &&\
    pip install -r requirements.txt
