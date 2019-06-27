FROM continuumio/miniconda3:4.5.12 as builder

ARG COMPUTE_API_VER

ARG VER

WORKDIR /build

COPY . .

ENV COMPUTE_API_VER=${COMPUTE_API_VER}

RUN echo "__version__ = '${VER}'" > cwt_cert/_version.py && \
      conda install -c conda-forge conda-build && \
      conda build -c conda-forge -c cdat --output-folder /output conda/

FROM builder as uploader

ARG VER

RUN conda install -c conda-forge anaconda-client

ENV VER=${VER}

CMD ["/bin/bash", "-c", "anaconda login && anaconda upload /output/noarch/esgf-compute-cert-${VER}-py_0.tar.bz2 -u cdat --force"]

FROM continuumio/miniconda3:4.5.12

COPY --from=builder /output/noarch/* /opt/conda/conda-bld/noarch/

RUN conda install -c conda-forge -c cdat --use-local esgf-compute-cert=${VER}

ENTRYPOINT ["cwt-cert"]
