import shutil
from pathlib import Path

from htmlnode import HTMLNode
from textnode import TextNode, TextType


def find_project_root(start: Path, marker: str = "public") -> Path:
    for parent in [start, *start.parents]:
        if (parent / marker).exists():
            return parent
    raise RuntimeError("Project root not found")


HERE = Path(__file__).resolve()
PROJECT_ROOT = find_project_root(HERE)

STATIC_DIR = PROJECT_ROOT / "static"
PUBLIC_DIR = PROJECT_ROOT / "public"


def deploy(source: Path, destination: Path):
    shutil.rmtree(destination)
    shutil.copytree(source, destination)


if __name__ == "__main__":
    deploy(STATIC_DIR, PUBLIC_DIR)
