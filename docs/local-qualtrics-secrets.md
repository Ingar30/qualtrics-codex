# Local Qualtrics Secrets

You do not need Qualtrics credentials for the synthetic smoke test, unit tests, or GitHub Pages demo. Add credentials only when you are ready to make live Qualtrics API calls from your own machine.

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
python scripts/qualtrics_workflow.py list-surveys
```

Create, activate, modify, or delete live surveys only after you explicitly ask Codex to do that action.
