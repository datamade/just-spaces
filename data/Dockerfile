FROM python:3.7-slim-stretch

RUN mkdir -p /usr/local/src
WORKDIR /usr/local/src

COPY requirements.txt /usr/local/src/

RUN set -ex \
	&& buildDeps=" \
		build-essential \
	" \
	&& deps=" \
		unzip \
		make \
		wget \
	" \
	&& apt-get update && apt-get install -y $deps $buildDeps --no-install-recommends \
	&& pip install --no-cache-dir -r requirements.txt \
	&& apt-get purge -y --auto-remove $buildDeps \
	&& rm  -Rf /var/lib/apt/lists/*

COPY . /usr/local/src

ENTRYPOINT ["make"]
