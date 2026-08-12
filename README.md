# Download Hou, Xue and Zhang (HXZ) data

A simple Python package for downloading HXZ data (including vintage data).

## Installation

I will not release a PyPI package. Therefore, you can install `hxz_download` directly from the GitHub repository using `pip`:

```bash
pip install git+https://github.com/mk0417/hou-xue-zhang-download.git
```

## Usage

```python
import hxz_download as hxz
```

To view all available :

```python
avail_factor_version = hxz.list_factor_versions()
avail_port_version = hxz.list_port_versions()
avail_themes = hxz.list_themes()
avail_freq = hxz.list_freq()
```

To download details of factors:

```python
hxz.doc_dl()
```

Use `factor_dl` to download factor returns, and use `port_dl` to download portfolio returns of all anomalies.

```python
# Download monthly factor returns (sample ends in 2025 that is released in 2026)
data = hxz.factor_dl('monthly', 2025)

# Download yearly portfolio returns of all anomalies in momentum theme
data = hxz.port_dl('mom', 'annual', 2025)
```

## Data source

- https://global-q.org/factors.html
- https://global-q.org/testingportfolios.html

