#!/usr/bin/env python3

import json
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen
import re


ROOT = Path(__file__).resolve().parents[1]
SOFTWARE_FILE = ROOT / "data" / "software.json"
CITATIONS_FILE = ROOT / "data" / "citations.json"

USER_AGENT = (
    "OmilletLab-Software-Portal/1.0 "
    "(https://github.com/omilletlab/software)"
)


def fetch_doi_format(doi, accept):
    doi_url = f"https://doi.org/{quote(doi, safe='/')}"

    request = Request(
        doi_url,
        headers={
            "Accept": accept,
            "User-Agent": USER_AGENT,
        },
    )

    try:
        with urlopen(request, timeout=30) as response:
            return response.read().decode("utf-8").strip()
    except HTTPError as exc:
        raise RuntimeError(
            f"DOI request for {doi} failed with HTTP {exc.code}"
        ) from exc
    except URLError as exc:
        raise RuntimeError(
            f"Could not retrieve citation data for {doi}: {exc.reason}"
        ) from exc


def load_software():
    with SOFTWARE_FILE.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def collect_publications(software):
    publications = {}

    for item in software:
        software_id = item.get("id", "<unknown>")

        for publication in item.get("publications", []):
            publication_id = publication.get("id")

            if not publication_id:
                raise ValueError(
                    f"Publication in {software_id} has no id."
                )

            if publication_id in publications:
                raise ValueError(
                    f"Duplicate publication id: {publication_id}"
                )

            publications[publication_id] = publication

    return publications


def collect_citation_ids(software):
    citation_ids = []

    for item in software:
        software_id = item.get("id", "<unknown>")

        for citation_id in item.get("citations", []):
            citation_ids.append((software_id, citation_id))

    return citation_ids


def generate_citations(software):
    publications = collect_publications(software)
    citation_references = collect_citation_ids(software)

    result = {}

    for software_id, citation_id in citation_references:
        if citation_id in result:
            continue

        publication = publications.get(citation_id)

        if publication is None:
            raise ValueError(
                f"{software_id} references unknown citation "
                f"{citation_id!r}."
            )

        doi = publication.get("doi")

        if not doi:
            raise ValueError(
                f"Citation {citation_id!r} has no DOI."
            )

        print(f"Fetching {citation_id}: {doi}")

        citation = fetch_doi_format(
            doi,
            "text/x-bibliography; style=elsevier-vancouver; locale=en-US",
        )

        citation = re.sub(
            r"^\s*\[\d+\]\s*",
            "",
            citation,
        )

        bibtex = fetch_doi_format(
            doi,
            "application/x-bibtex",
        )

        result[citation_id] = {
            "doi": doi,
            "citation": citation,
            "bibtex": bibtex,
        }

    return result


def write_citations(citations):
    with CITATIONS_FILE.open("w", encoding="utf-8") as handle:
        json.dump(
            citations,
            handle,
            indent=2,
            ensure_ascii=False,
        )
        handle.write("\n")


def main():
    try:
        software = load_software()
        citations = generate_citations(software)
        write_citations(citations)
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    count = len(citations)
    noun = "entry" if count == 1 else "entries"

    print(
        f"Wrote {count} citation {noun} to "
        f"{CITATIONS_FILE.relative_to(ROOT)}"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
