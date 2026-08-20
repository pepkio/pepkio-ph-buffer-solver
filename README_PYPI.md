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
result = client.run(client.get_example_input("phosphate_50mM_pH74"))
print(result.status)
```
