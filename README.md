# pepkio-ph-buffer-solver

Python client and CLI for Pepkio's `ph-buffer-solver` tool.

## Installation

```bash
pip install pepkio-ph-buffer-solver
```

## Quickstart

```python
from pepkio_ph_buffer_solver import PepkioClient

client = PepkioClient(api_key="your_api_key")
manifest = client.get_manifest()
print(manifest["title"])
```
