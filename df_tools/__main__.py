import click
from pathlib import Path
import nbformat
import sys
import asyncio
from nbconvert import MarkdownExporter, HTMLExporter, NotebookExporter, preprocessors
from black import format_str, FileMode, InvalidInput
import re

from traitlets.config import Config
from nbconvert.preprocessors import ClearOutputPreprocessor

FILE_PATTERN = re.compile(r"^[0-9]{2}\w?-[a-zA-Z-]+$")

# See https://bugs.python.org/issue37373 :(
if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

@click.group()
def cli():
    pass


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
        with open(notebook, encoding="utf8") as nb_file:
            nb = nbformat.read(nb_file, as_version=4)
        executor.preprocess(nb)

        if not nb.cells[-1]["source"]:
            nb.cells.pop()

        markdown, _ = exporter.from_notebook_node(nb)
        with open(f"{notebook.stem}.md", "w", encoding="utf8") as writable:
            writable.write(markdown)


@cli.command()
def html():
    executor = preprocessors.ExecutePreprocessor()
    exporter = HTMLExporter()
    for notebook in get_files("ipynb"):
        with open(notebook, encoding="utf8") as nb_file:
            nb = nbformat.read(nb_file, as_version=4)
        executor.preprocess(nb)

        if not nb.cells[-1]["source"]:
            nb.cells.pop()
        html, _ = exporter.from_notebook_node(nb)
        with open(f"{notebook.stem}.html", "w", encoding="utf8") as writable:
            writable.write(html)


def _delete_generated_files():
    for md in get_files("md"):
        md.unlink()
    for html in get_files("html"):
        html.unlink()


def format_code_cells(notebobk):
    file_mode = FileMode()
    for cell in notebobk.cells:
        if cell["cell_type"] == "code":
            tags = cell.get("metadata", dict()).get("tags", [])
            if "not-formatted" not in tags:
                try:
                    result = format_str(cell["source"], mode=file_mode)
                    if result[-1] == "\n" and cell["source"] != "\n":
                        result = result[:-1]
                        cell["source"] = result
                except InvalidInput:
                    pass


@cli.command()
def clean():
    _delete_generated_files()
    config = Config()
    config.NotebookExporter.preprocessors = [ClearOutputPreprocessor()]
    exporter = NotebookExporter(config=config)

    for notebook in get_files("ipynb"):
        with open(notebook, encoding="utf8") as nb_file:
            nb = nbformat.read(nb_file, as_version=4)

        if not nb.cells[-1]["source"]:
            nb.cells.pop()

        format_code_cells(nb)

        for cell_id, cell in enumerate(nb.cells):
            cell["id"] = f"{notebook.stem}-{cell_id}"

        ipynb, _ = exporter.from_notebook_node(nb)
        with open(f"{notebook.stem}.ipynb", "w", encoding="utf8") as writable:
            writable.write(ipynb)


if __name__ == "__main__":
    cli()
