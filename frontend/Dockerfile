FROM python:alpine3.15

ENV PYTHONUNBUFFERED=1
LABEL maintainer 0805004949

RUN addgroup app && adduser -SG app app
USER app
WORKDIR /frontend

# # shell prompt highlighting
RUN echo "alias egrep='egrep --color=auto'" >> ~/.basshrc && \
    echo "alias fgrep='fgrep --color=auto'" >> ~/.bashrc && \
    echo "alias grep='grep --color=auto'" >> ~/.bashrc  && \
    echo "alias l='ls -CF'" >> ~/.bashrc && \
    echo "alias la='ls -A'" >> ~/.bashrc && \
    echo "alias ll='ls -alF'" >> ~/.bashrc && \
    echo "alias ls='ls --color=auto'" >> ~/.bashrc

EXPOSE 5000
EXPOSE 8000

COPY . /frontend
