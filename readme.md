# docsend

Convert docsend.com to PDF or PNG image sequence.

## Install

Python 3.6+ is required.

```
pip install docsend
```

## Usage

From command line:

```shell
# download a pdf
docsend doc_id --email me@example.com

# include passcode if required
docsend doc_id -e me@example.com --passcode 123example123

# download png sequence
docsend doc_id -e me@example.com --format png

# specify output file or directory name
docsend doc_id -e me@example.com -f pdf --output doc.pdf

# all options combined
docsend doc_id -e me@example.com -p 123example123 -f png -o pages
```

From Python code:

```python
from docsend import DocSend

ds = DocSend('abcdef9')
ds.fetch_meta()
ds.authorize('me@example.com')
ds.fetch_images()
ds.save_pdf('doc.pdf')
ds.save_images('pages')
```

## Missing features

You are welcome to contribute.

## Contributing & Developing

Open the repo in Github Codespaces:

```
# Install jpeg lib dependencies missing in Codespaces
sudo apt-get install libjpeg-dev zlib1g-dev

# Install poetry
pip install poetry

# Install project dependencies
poetry install

# Activate the environment
poetry shell
```