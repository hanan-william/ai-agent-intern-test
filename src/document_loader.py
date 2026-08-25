import re
from pathlib import Path


KNOWLEDGE_BASE_DIR = (
    Path(__file__).resolve().parents[1] / "knowledge-base"
)


def parse_front_matter(text: str) -> tuple[dict, str]:
    """
    Extract YAML-like metadata from the beginning of a Markdown file.

    Returns:
        metadata: dictionary containing document metadata
        content: Markdown content after the front matter
    """
    pattern = r"^---\s*\n(.*?)\n---\s*\n(.*)$"

    match = re.match(pattern, text, re.DOTALL)

    if not match:
        return {}, text

    raw_metadata = match.group(1)
    content = match.group(2)

    metadata = {}

    for line in raw_metadata.splitlines():
        if ":" not in line:
            continue

        key, value = line.split(":", 1)

        metadata[key.strip()] = value.strip()

    return metadata, content


def load_knowledge_base() -> list[dict]:
    """
    Load all Markdown documents from the knowledge base.
    """
    documents = []

    for file_path in sorted(KNOWLEDGE_BASE_DIR.glob("*.md")):
        text = file_path.read_text(encoding="utf-8")

        metadata, content = parse_front_matter(text)

        documents.append(
            {
                "source": file_path.name,
                "metadata": metadata,
                "content": content.strip(),
            }
        )

    return documents