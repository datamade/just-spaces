FROM quay.io/azavea/django:2.0-python3.6-slim

RUN mkdir -p /usr/local/src
WORKDIR /usr/local/src

COPY requirements.txt /usr/local/src/

RUN set -ex \
	&& buildDeps=" \
		build-essential \
	" \
	&& deps=" \
		git \
	" \
	&& apt-get update && apt-get install -y $deps $buildDeps --no-install-recommends \
	&& pip install --no-cache-dir -U -r requirements.txt \
	&& apt-get purge -y --auto-remove $buildDeps \
	&& rm  -Rf /var/lib/apt/lists/*

COPY . /usr/local/src

ENTRYPOINT ["python"]
