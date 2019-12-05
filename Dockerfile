FROM panwenbin/fxt-python2

COPY download_center-5.2.1-py2-none-any.whl download_center-5.2.1-py2-none-any.whl

RUN pip install download_center-5.2.1-py2-none-any.whl

ADD . /app

WORKDIR /app