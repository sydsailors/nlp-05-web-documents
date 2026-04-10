"""
src/nlp/stage02_validate_sailors.py - Validate Stage
(EDIT YOUR COPY OF THIS FILE)

Source: Raw HTML string
Sink:   BeautifulSoup object (in memory)

Purpose

  Validates that the expected page structure is present.

Analytical Questions

- What is the top-level structure of the HTML document?
- What elements are present in the document?
- What data types are associated with each field?
- Does the data meet expectations for transformation?

Notes

Following our process, do NOT edit this _case file directly,
keep it as a working example.

In your custom project, copy this _case.py file and
append with _yourname.py instead.

Then edit your copied Python file to:
- inspect the JSON structure for your API,
- validate required keys and types,
- confirm the data is usable for your analysis.
"""

# ============================================================
# Section 1. Setup and Imports
# ============================================================

import logging

from bs4 import BeautifulSoup

# ============================================================
# Section 2. Define Run Validate Function
# ============================================================


def run_validate(
    html_content: str,
    LOG: logging.Logger,
) -> BeautifulSoup:
    """Inspect and validate HTML structure.

    Args:
        html_content (str): The raw HTML content from the Extract stage.
        LOG (logging.Logger): The logger instance.

    Returns:
        BeautifulSoup: The validated BeautifulSoup object.
    """
    LOG.info("========================")
    LOG.info("STAGE 02: VALIDATE starting...")
    LOG.info("========================")

    # ============================================================
    # INSPECT HTML STRUCTURE
    # ============================================================

    LOG.info("HTML STRUCTURE INSPECTION:")

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Log the type of the top-level HTML structure.
    LOG.info(f"Top-level type: {type(soup).__name__}")

    # Log the top-level elements in the HTML document
    LOG.info(
        f"Top-level elements: {[element.name for element in soup.find_all(recursive=False)]}"
    )

    # ============================================================
    # VALIDATE EXPECTATIONS
    # ============================================================

    # Check for expected structural elements

    title = soup.find("h1")
    author = soup.find("h2")
    chapter_divs = soup.find_all("div", class_="chapter")

    LOG.info("VALIDATE: Title (h1) found: %s", title is not None)
    LOG.info("VALIDATE: Author (h2) found: %s", author is not None)
    LOG.info("VALIDATE: Chapter content found: %s", chapter_divs is not None)

    paragraphs = []
    for div in chapter_divs:
        paragraphs.extend(div.find_all("p"))

    LOG.info("VALIDATE: Chapter count: %d", len(chapter_divs))
    LOG.info("VALIDATE: Total paragraph count: %d", len(paragraphs))

    missing = []
    if not title:
        missing.append("title")
    if not author:
        missing.append("author")
    if not chapter_divs:
        missing.append("chapter content")
    if len(paragraphs) < 200:
        missing.append("sufficient paragraph text")

    if missing:
        raise ValueError(
            f"VALIDATE: Required elements missing or insufficient: {missing}. "
            "Page structure may have changed."
        )

    LOG.info("VALIDATE: HTML structure is valid for Project Gutenberg.")
    LOG.info("Sink: validated BeautifulSoup object")

    return soup
