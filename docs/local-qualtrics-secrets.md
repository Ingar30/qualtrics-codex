# Local Qualtrics Secrets

You do not need Qualtrics credentials for offline checks, unit tests, or GitHub Pages. Add credentials only when you are ready to make live Qualtrics API calls from your own machine.

Never commit API tokens, `.env` files, `.secrets/` folders, raw response exports, survey metadata, or reusable survey links.

## Required Values

The live Qualtrics scripts read these environment variables:

```text
QUALTRICS_DATACENTER
QUALTRICS_API_TOKEN
```

Optional:

```text
QUALTRICS_PUBLIC_HOST
```

`QUALTRICS_DATACENTER` is the datacenter part used for your Qualtrics API host. `QUALTRICS_PUBLIC_HOST` is useful when your reusable survey links use a branded host.

## Find Your Qualtrics API Details

Qualtrics' official API overview is here:

```text
https://www.qualtrics.com/support/integrations/api-integration/overview/
```

To find or generate an API token, Qualtrics directs users to:

```text
User settings icon -> Account Settings -> Qualtrics IDs -> API -> Generate Token
```

Your account must have the `Access API` permission enabled. If you already have a token, do not generate a new one casually: replacing a token can break tools that use the old token.

For `QUALTRICS_DATACENTER`, use the datacenter part of the API base URL. If the API host is:

```text
https://yourdatacenterid.qualtrics.com/API/v3
```

then set:

```text
QUALTRICS_DATACENTER=yourdatacenterid
```

Do not include `https://`, `.qualtrics.com`, or `/API/v3` in `QUALTRICS_DATACENTER`.

## Windows PowerShell

Create a secrets folder outside the repository:

```powershell
New-Item -ItemType Directory -Force $HOME\.secrets
notepad $HOME\.secrets\qualtrics.env.ps1
```

Put this in `$HOME\.secrets\qualtrics.env.ps1`:

```powershell
$env:QUALTRICS_DATACENTER = "your_datacenter"
$env:QUALTRICS_API_TOKEN = "your_token"
$env:QUALTRICS_PUBLIC_HOST = "yourbrand.qualtrics.com"
```

Load it before live API calls:

```powershell
. $HOME\.secrets\qualtrics.env.ps1
```

Check that the required variables are present without printing their values:

```powershell
if ($env:QUALTRICS_DATACENTER -and $env:QUALTRICS_API_TOKEN) { "Qualtrics env vars are set" }
```

## macOS/Linux

Create a secrets folder outside the repository:

```bash
mkdir -p "$HOME/.secrets"
nano "$HOME/.secrets/qualtrics.env"
```

Put this in `$HOME/.secrets/qualtrics.env`:

```bash
export QUALTRICS_DATACENTER="your_datacenter"
export QUALTRICS_API_TOKEN="your_token"
export QUALTRICS_PUBLIC_HOST="yourbrand.qualtrics.com"
```

Load it before live API calls:

```bash
source "$HOME/.secrets/qualtrics.env"
```

Check that the required variables are present without printing their values:

```bash
test -n "$QUALTRICS_DATACENTER" && test -n "$QUALTRICS_API_TOKEN" && echo "Qualtrics env vars are set"
```

## Use With Codex

Do not paste token values into a Codex prompt. Tell Codex where your local secrets file is and ask it to verify that the expected environment variable names are present without printing values.

After loading the file, the first small live check is:

```bash
python scripts/qualtrics_workflow.py check-auth
```

Use `list-surveys` only when you explicitly need to browse surveys. By default, it hides survey IDs; use `--show-private-ids` only for local troubleshooting.

Create, activate, modify, or delete live surveys only after you explicitly ask Codex to do that action.
