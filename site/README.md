# Reference Web Interface

This static, dependency-free interface provides an indicative self-assessment and JSON export. It does not verify evidence and therefore does not independently establish Evidence-Based conformance.

From the repository root, run:

```bash
python -m http.server 8080
```

Then open `http://localhost:8080/site/`. For Docker, run `docker build -t eaims .` and `docker run --rm -p 8080:80 eaims`.
