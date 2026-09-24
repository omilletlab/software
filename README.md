# Omillet Lab Software

Public software portal for tools developed by the Precision Medicine & Metabolism Lab at CIC bioGUNE.

The portal provides a central entry point to the lab's released scientific software, including links to web applications, documentation, source code, publications, and citation information when available.

## Software catalogue

Software entries are defined in:

```text
data/software.json
```

The portal is generated dynamically from this catalogue.

Each entry may include:

* software name and description;
* current version;
* implementation languages;
* available interfaces;
* web application;
* documentation;
* GitHub repository;
* license and permitted-use information;
* citation information;
* associated publications.

## Development

The portal is a static site intended for deployment through GitHub Pages.

For local preview:

```bash
python3 -m http.server 8000
```

Then open:

```text
http://localhost:8000
```

## License

This software is available for academic and non-commercial research use.
Commercial use requires prior written authorization from CIC bioGUNE.

See the [LICENSE](LICENSE) file for details.
