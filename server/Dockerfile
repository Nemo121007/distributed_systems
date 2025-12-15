ARG BOINC_USER=boinc
ARG PROJECT_ROOT=/var/lib/boinc
FROM ubuntu:20.04

# Установка переменных окружения для неинтерактивной установки
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Moscow

# Установка базовых зависимостей, включая libzip-dev и Cython
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    git \
    build-essential \
    m4 \
    autoconf \
    automake \
    libtool \
    pkg-config \
    mysql-client \
    libmysqlclient-dev \
    apache2 \
    php \
    libapache2-mod-php \
    php-mysql \
    netcat-openbsd \
    nlohmann-json3-dev \
    libcurl4-openssl-dev \
    libfcgi-dev \
    libssl-dev \
    freeglut3-dev \
    libnotify-dev \
    libgtk-3-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libwebkit2gtk-4.0-dev \
    libzip-dev \
    && rm -rf /var/lib/apt/lists/*

# Установка Cython и других зависимостей для сборки pandas
RUN pip3 install --no-cache-dir Cython numpy

# Создание символической ссылки на python3
RUN ln -s /usr/bin/python3 /usr/bin/python

# Сборка wxWidgets из исходников
RUN git clone --branch v3.1.5 https://github.com/wxWidgets/wxWidgets.git /opt/wxWidgets
WORKDIR /opt/wxWidgets
RUN git submodule update --init --recursive
RUN ./configure --enable-shared --enable-unicode
RUN make -j$(nproc)
RUN make install

# Создание пользователя BOINC с явным указанием имени
RUN useradd -m -d /var/lib/boinc -s /bin/bash boinc

# Установка переменных окружения после создания пользователя
ENV BOINC_USER=boinc
ENV PROJECT_ROOT=/var/lib/boinc

# Установка BOINC из исходников
RUN git clone https://github.com/BOINC/boinc.git /opt/boinc
WORKDIR /opt/boinc
RUN ./_autosetup
RUN ./configure --disable-client --enable-server
# Очистка перед сборкой
RUN make clean
# Последовательная сборка без параллелизации
RUN make
RUN make install

# Создание директории проекта
RUN mkdir -p $PROJECT_ROOT && chown $BOINC_USER:$BOINC_USER $PROJECT_ROOT

# Копирование requirements.txt
COPY app/requirements.txt /tmp/
# Установка numpy перед pandas, так как pandas зависит от numpy
RUN pip3 install --no-cache-dir numpy
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

# Копирование скриптов и шаблонов
COPY server/init_project.sh /usr/local/bin/
COPY server/create_work.sh /usr/local/bin/
COPY server/templates/ /var/lib/boinc/templates/

RUN chmod +x /usr/local/bin/init_project.sh /usr/local/bin/create_work.sh

# Переключение на пользователя BOINC
USER boinc
WORKDIR $PROJECT_ROOT

ENTRYPOINT ["/usr/local/bin/init_project.sh"]