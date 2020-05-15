import click


@click.group()
def oai():
    """OAI harvester commands"""


@oai.group()
def register():
    pass


@register.command("provider")
def register_provider():
    pass
