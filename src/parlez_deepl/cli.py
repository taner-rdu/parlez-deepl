# cli.py — defines the command-line interface for parlez-deepl
# Uses click to turn Python functions into terminal commands

import os
import click
from parlez_deepl import DeepLClient

# @click.group() makes `main` a command group (i.e. `parlez-deepl <subcommand>`)
@click.group()
def main():
    pass

# Registers `translate` as a subcommand of the `main` group
@main.command()
# Positional argument — required, e.g. `parlez-deepl translate "hello"`
@click.argument("text")
# Named option — e.g. `--target-lang FR`
@click.option("--target-lang", required=True, help="Target language code (e.g. FR, DE)")
def translate(text, target_lang):
    """Translate TEXT to the target language."""
    # Read API key from environment — fails early with a clear message if missing
    api_key = os.environ.get("DEEPL_API_KEY")
    if not api_key:
        raise click.ClickException("DEEPL_API_KEY environment variable is not set")

    # Instantiate the SDK client with the API key
    client = DeepLClient(api_key=api_key)

    # Call the translate method and print the result
    result = client.translate(text, target_lang=target_lang)
    click.echo(result)