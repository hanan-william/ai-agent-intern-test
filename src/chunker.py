import re


def chunk_document(document: dict) -> list[dict]:
    """
    Split a Markdown document into sections.

    Each section keeps the original document metadata and source.
    """
    content = document["content"]

    sections = re.split(r"(?m)^## ", content)

    chunks = []

    for section in sections:
        section = section.strip()

        if not section:
            continue

        lines = section.splitlines()

        heading = lines[0].strip()
        body = "\n".join(lines[1:]).strip()

        if not body:
            continue

        chunks.append(
            {
                "source": document["source"],
                "metadata": document["metadata"],
                "heading": heading,
                "content": body,
            }
        )

    return chunks