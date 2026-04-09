import os
import shutil
import sys
from pathlib import Path
from re import T

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


def generate_page(
    from_path: Path, template_path: Path, dest_path: Path, base_path: str
):
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
    template = template.replace('href="/', f'href="{base_path}')
    template = template.replace('src="/', f'src="{base_path}')
    rel_path = from_path.relative_to(CONTENT_DIR)
    dest_file = dest_path / rel_path.parent / f"{rel_path.stem}.html"
    if dest_file.exists():
        dest_file.unlink()
    dest_file.parent.mkdir(parents=True, exist_ok=True)
    with open(dest_file, "w") as f:
        f.write(template)


def generate_pages_recursive(
    content_path: Path, template_path: Path, dest_dir_path: Path, base_path: str
):
    for root, dirs, files in os.walk(content_path):
        for file in files:
            generate_page(Path(root) / file, template_path, dest_dir_path, base_path)


def deploy_static(source: Path, destination: Path):
    shutil.rmtree(destination)
    shutil.copytree(source, destination)


def deploy_content(source: Path, destination: Path, base_path: str):
    generate_pages_recursive(
        source, PROJECT_ROOT / "template.html", destination, base_path
    )


if __name__ == "__main__":
    base_path = sys.argv[0] if len(sys.argv) > 0 else "/"
    deploy_static(STATIC_DIR, PUBLIC_DIR)
    deploy_content(CONTENT_DIR, PUBLIC_DIR, base_path)
