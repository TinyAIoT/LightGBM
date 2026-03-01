## Troubleshooting

### `get_dataset.py`
Mac sometimes experiences ceritficates issues.
`urllib.error.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: Missing Subject Key Identifier (_ssl.c:1032)>`
Quick but not secure fix is to include:

```python
ssl._create_default_https_context = ssl._create_unverified_context
```
