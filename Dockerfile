FROM jupyter/base-notebook:python-3.8.8 as base

WORKDIR /workspace

COPY Pipfile.lock Pipfile ./

RUN pip install pipenv && \
    pipenv install --system --deploy --ignore-pipfile

CMD ["jupyter", "lab"]

FROM base AS self-contained

COPY *.ipynb ./
