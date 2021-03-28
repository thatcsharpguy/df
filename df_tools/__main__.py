import click
from pathlib import Path
import nbformat
from nbconvert import MarkdownExporter, NotebookExporter, preprocessors
import re

from nbconvert.preprocessors import ClearOutputPreprocessor

FILE_PATTERN = re.compile(r"^[0-9]{2}\w?-[a-zA-Z-]+$")


@click.group()
def cli():
    pass


from traitlets.config import Config

c = Config()
c.NotebookExporter.preprocessors = [ClearOutputPreprocessor()]


def get_files(extension: str):
    for file in Path(".").glob(f"*.{extension}"):
        if not FILE_PATTERN.match(file.stem):
            continue
        yield file


@cli.command()
def markdown():
    executor = preprocessors.ExecutePreprocessor()
    exporter = MarkdownExporter()
    for notebook in get_files("ipynb"):
        with open(notebook) as nb_file:
            nb = nbformat.read(nb_file, as_version=4)
        executor.preprocess(nb)

        if not nb.cells[-1]["source"]:
            nb.cells.pop()

        markdown, _ = exporter.from_notebook_node(nb)
        with open(f"{notebook.stem}.md", "w") as writable:
            writable.write(markdown)


@cli.command()
def clean():
    for md in get_files("md"):
        md.unlink()

    exporter = NotebookExporter(config=c)
    for notebook in get_files("ipynb"):

        with open(notebook) as nb_file:
            nb = nbformat.read(nb_file, as_version=4)

        if not nb.cells[-1]["source"]:
            nb.cells.pop()

        for cell_id, cell in enumerate(nb.cells):
            cell["id"] = f"{notebook.stem}-{cell_id}"

        ipynb, _ = exporter.from_notebook_node(nb)
        with open(f"{notebook.stem}.ipynb", "w") as writable:
            writable.write(ipynb)


if __name__ == "__main__":
    cli()
