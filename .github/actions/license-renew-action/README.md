# License renew action

This action increment the year in your `LICENSE` file

## Inputs

### `license-path`

**Required** Github token to submit PR.
**Optional** Path to your license file. Default `LICENSE`.

## Example usage

uses: actions/license-renew-action@v1
with:
  license-path: 'LICENSE.md'
