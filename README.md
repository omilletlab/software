# Omillet Lab Software

Public software portal for tools developed by the Precision Medicine & Metabolism Lab at CIC bioGUNE.

The portal provides a central entry point to the lab's scientific software, including links to web applications, documentation, source code, publications, licenses, and citation information when available.

## Software catalogue

Software entries are defined in:

```text
data/software.json
```

The portal is rendered dynamically from this catalogue.

Each software entry may include:

- software name and description;
- current version;
- implementation languages;
- available interfaces;
- web application;
- documentation;
- GitHub repository;
- license and permitted-use information;
- associated publications;
- publications recommended for citation.

Fields that are not applicable or not yet available may be left empty or set to `null`, depending on the field.

## Publications and citations

Associated publications are stored inside each software entry in `data/software.json`.

Each publication should have a stable internal `id`, for example:

```json
{
  "id": "example-paper",
  "label": "Primary publication",
  "title": "Example publication title",
  "doi": "10.xxxx/example",
  "url": "https://doi.org/10.xxxx/example"
}
```

Publications that users should cite when using the software are referenced by their publication IDs:

```json
"citations": [
  "example-paper"
]
```

This keeps publication metadata in a single location and avoids duplicating DOI or title information.

### Generated citation data

Formatted citations and BibTeX entries are generated automatically from DOI metadata.

Run:

```bash
python3 scripts/update_citations.py
```

The script reads the citation references in `data/software.json` and generates:

```text
data/citations.json
```

The generated file is used by the portal to provide:

- a formatted citation that can be copied;
- a downloadable BibTeX file.

Do not edit generated citation text or BibTeX manually. Update the DOI or citation references in `data/software.json` and run the script again instead.

## Adding software

To add a new software entry:

1. Add the software metadata to `data/software.json`.
2. Add any associated publications.
3. Reference the publications that should be cited using the `citations` array.
4. Run:

```bash
python3 scripts/update_citations.py
```

5. Validate both JSON files:

```bash
python3 -m json.tool data/software.json > /dev/null
python3 -m json.tool data/citations.json > /dev/null
```

6. Preview the portal locally before publishing.

## Development

The portal is a dependency-free static site built with HTML, CSS, and vanilla JavaScript.

There is no build step.

For local preview, run from the repository root:

```bash
python3 -m http.server 8000
```

Then open:

```text
http://localhost:8000
```

The portal should be served over HTTP because the software catalogue and generated citation data are loaded with `fetch()`.

Before considering a change complete, also run:

```bash
git diff --check
```

## Deployment

The portal is intended for deployment through GitHub Pages.

The deployed site is generated directly from the static repository contents; no application server or build pipeline is required.

## License

This software portal is available for academic and non-commercial research use.

Commercial use requires prior written authorization from CIC bioGUNE.

See the [LICENSE](LICENSE) file for details.
