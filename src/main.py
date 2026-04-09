import shutil
from pathlib import Path

from utils import extract_title, markdown_to_html_node


def find_project_root(start: Path, marker: str = "public") -> Path:
    for parent in [start, *start.parents]:
        if (parent / marker).exists():
            return parent
    raise RuntimeError("Project root not found")


HERE = Path(__file__).resolve()
PROJECT_ROOT = find_project_root(HERE)

STATIC_DIR = PROJECT_ROOT / "static"
PUBLIC_DIR = PROJECT_ROOT / "public"
CONTENT_DIR = PROJECT_ROOT / "content"


def generate_page(from_path: Path, template_path: Path, dest_path: Path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        md = f.read()
    with open(template_path, "r") as f:
        template = f.read()
    node = markdown_to_html_node(md)
    html = node.to_html()
    title = extract_title(md)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    dest_file = dest_path / "index.html"
    if dest_file.exists():
        dest_file.unlink()
    with open(dest_file, "w") as f:
        f.write(template)


def deploy(source: Path, destination: Path):
    shutil.rmtree(destination)
    shutil.copytree(source, destination)
    generate_page(CONTENT_DIR / "index.md", PROJECT_ROOT / "template.html", destination)


if __name__ == "__main__":
    deploy(STATIC_DIR, PUBLIC_DIR)
