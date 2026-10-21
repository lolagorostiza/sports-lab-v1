# Chaos Sports Lab — my route

> Repository created from the Bitexoft template. Replace this text with your own: this
> README is the first thing an interviewer looks at.

## What it does

One line about what the project builds, in your words.

## How to run it

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
python -m chaoslab analyze data/sample.csv
```

## How it is verified

```bash
pip install bitexoft-verify
bitexoft-verify check A1        # seconds, while you work
```

The result that counts is CI's: push and look at the *Actions* tab. The report
(`verify-report.json`) is kept as a run artifact; import it into the platform to mark the
delivery.

## Deliveries

One git tag per delivery, so later ones can compare against earlier ones:

```bash
git tag A1 && git push --tags
```

| Delivery | State | What it adds |
|---|---|---|
| A1 | | |

## What I do NOT claim

The most valuable section of the repository in an interview. What is not validated, what
assumptions the model carries, what you measured and what you eyeballed. Write it as you
go, not at the end.

## Data sources

If you use third-party data, cite it here and respect its terms of use.
