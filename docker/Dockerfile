FROM continuumio/miniconda3:4.5.12 as builder

WORKDIR /build

COPY . .

RUN conda install -c conda-forge conda-build && \
      conda build -c conda-forge -c cdat conda/

FROM continuumio/miniconda3:4.5.12

COPY --from=builder /opt/conda/conda-bld/noarch/* /opt/conda/conda-bld/noarch/

RUN conda install -c conda-forge -c cdat --use-local esgf-compute-cert=devel

ENTRYPOINT ["cwt-cert"]
