"""
src/nlp/stage03_transform_sailors.py
(EDIT YOUR COPY OF THIS FILE)

Source: validated BeautifulSoup object
Sink: Pandas DataFrame

NOTE: We use Pandas here to contrast with Polars (from Module 4).
You may use Polars or another library if you prefer:
the pipeline pattern is identical; only the DataFrame API differs.

Pandas vs. Polars:
- Pandas is widely used and has a larger ecosystem.
- Polars is faster, more memory efficient, handles larger datasets,
  and is better suited for production pipelines and complex
  transformations.

Purpose

  Transform validated BeautifulSoup object into a structured format.

Analytical Questions

- Which fields are needed from the HTML data?
- How can records be normalized into tabular form?
- What derived fields would support analysis?

How to find the fields you want to extract from the web page:

  1. Open the web page in your browser.
  2. Right-click anywhere on the page and select "View Page Source".
  3. Use Ctrl+F to search for text you can see on the page,
     e.g. the paper title or "Abstract:".
  4. Find the HTML tag and class that wraps it, e.g.:
       <h1 class="title mathjax"><span class="descriptor">Title:</span>
  5. Use soup.find("h1", class_="title") to locate the associated tag.
  6. Use .get_text(strip=True) to extract the visible text from inside the tag.
  7. If the tag contains a descriptor prefix like "Title:" or "Authors:",
     use .replace("Title:", "").strip() to remove it.
  8. If the tag is not found, soup.find() returns None which is not a string.
     To avoid errors, use a conditional expression to return "unknown" as a safe fallback:
       value = tag.get_text(strip=True) if tag else "unknown"

Apply this process for each field you want to extract for analysis.
The same approach works for any web page.

Example: For the arXiv page at https://arxiv.org/abs/2602.20021,
we can extract the following fields using BeautifulSoup:

- title from <h1 class="title"> (string)
- authors from <div class="authors"> (string)
- abstract from <blockquote class="abstract"> (string)
- primary subject from <div class="subheader"> (string)
- submission date from <div class="dateline"> (string)
- arXiv ID from canonical link in the <head> section (string)

we can calculate derived fields like:
- abstract word count (integer)
- author count (integer)

IMPORTANT: Getting information from a web page is not as simple as it looks.
Web pages are designed for human consumption, not for data extraction.
The HTML structure can be complex and inconsistent, and may require careful inspection and handling to extract the desired information.
The title and abstract are wrapped in tags with descriptor text ("Title:", "Abstract:") that must be removed to get clean values.
The authors are listed as multiple <a> tags inside a <div>, so we must extract each author separately and join them with commas to avoid double-comma issues.
The arXiv ID is not directly visible on the page but can be extracted from the canonical link in the HTML head.
This stage requires careful inspection of the HTML structure and thoughtful handling of edge cases to ensure we extract clean, structured data for analysis.

Use all your resources, creativity, and problem-solving skills to navigate the complexities of web data extraction and transformation.

Notes

Following our process, do NOT edit this _case file directly,
keep it as a working example.

In your custom project, copy this _case.py file and
append with _yourname.py instead.

Then edit your copied Python file to:
- extract the fields needed for your analysis,
- normalize records into a consistent structure,
- create any derived fields required.
"""

# ============================================================
# Section 1. Setup and Imports
# ============================================================

import logging

from bs4 import BeautifulSoup, Tag
import pandas as pd

# ============================================================
# Section 2. Define Run Transform Function
# ============================================================


def run_transform(
    soup: BeautifulSoup,
    LOG: logging.Logger,
) -> pd.DataFrame:
    """Transform HTML into a structured DataFrame.

    Args:
        soup (BeautifulSoup): Validated BeautifulSoup object.
        LOG (logging.Logger): The logger instance.

    Returns:
        pd.DataFrame: The transformed dataset.
    """
    LOG.info("========================")
    LOG.info("STAGE 03: TRANSFORM starting...")
    LOG.info("========================")

    LOG.info("Extracting literary metadata and text from HTML")

    LOG.info("========================")
    LOG.info("STAGE 03a: Extract bibliographic fields")
    LOG.info("========================")

    title_tag: Tag | None = soup.find("h1")
    author_tag: Tag | None = soup.find("h2")

    title: str = title_tag.get_text(strip=True) if title_tag else "unknown"
    author: str = (
        author_tag.get_text(strip=True).replace("by ", "") if author_tag else "unknown"
    )

    LOG.info(f"Extracted title: {title}")
    LOG.info(f"Extracted author: {author}")

    # ============================================================
    # STAGE 03b: Extract main text
    # ============================================================

    chapter_div: Tag | None = soup.find("div", class_="chapter")

    paragraph_tags: list[Tag] = chapter_div.find_all("p") if chapter_div else []

    paragraphs: list[str] = [p.get_text(strip=True) for p in paragraph_tags]

    full_text: str = "\n".join(paragraphs)

    LOG.info(f"Extracted paragraph count: {len(paragraphs)}")
    LOG.info(f"Extracted text length (chars): {len(full_text)}")

    # ============================================================
    # STAGE 03c: Derived text analytics
    # ============================================================

    word_count: int = len(full_text.split())
    paragraph_count: int = len(paragraphs)
    avg_words_per_paragraph: float = (
        round(word_count / paragraph_count, 2) if paragraph_count > 0 else 0.0
    )

    LOG.info(f"Calculated word count: {word_count}")
    LOG.info(f"Calculated avg words per paragraph: {avg_words_per_paragraph}")

    # ============================================================
    # STAGE 03d: Build record and DataFrame
    # ============================================================

    record = {
        "title": title,
        "author": author,
        "paragraph_count": paragraph_count,
        "word_count": word_count,
        "avg_words_per_paragraph": avg_words_per_paragraph,
        "text": full_text,
    }

    df = pd.DataFrame([record])

    LOG.info(f"Created DataFrame with {len(df)} row and {len(df.columns)} columns")
    LOG.info(f"Columns: {list(df.columns)}")
    LOG.info(f"DataFrame preview:\n{df.head()}")

    LOG.info("Sink: Pandas DataFrame created")
    LOG.info("Transformation complete.")

    return df
