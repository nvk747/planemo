"""Module describing the planemo ``recipe_init`` command."""
import click

from planemo import github_util
from planemo import options
from planemo.cli import command_function
from planemo.config import planemo_option


CLONE_GITHUB_TARGETS = {
    "tools-iuc": "galaxyproject/tools-iuc",
    "tools-devteam": "galaxyproject/tools-devteam",
    "galaxy": "galaxyproject/galaxy",
    "planemo": "galaxyproject/planemo",
    "tools-galaxyp": "galaxyproteomics/tools-galaxyp",
    "bioconda-recipes": "bioconda/bioconda-recipes",
    "homebrew-science": "Homebrew/homebrew-science",
    "workflows": "common-workflow-language/workflows",
}


def clone_target_arg():
    """Represent target to clone/branch."""
    return click.argument(
        "target",
        metavar="TARGET",
        type=click.STRING,
    )


@click.command('clone')
@planemo_option(
    "--fork/--skip_fork",
    default=True,
    is_flag=True,
)
@planemo_option(
    "--branch",
    type=click.STRING,
    default=None,
    help="Create a named branch on result."
)
@clone_target_arg()
@options.optional_project_arg(exists=None, default="__NONE__")
@command_function
def cli(ctx, target, path, **kwds):
    """Short-cut to quickly clone, fork, and branch a relevant Github repo.

    For instance, the following will clone, fork, and branch the tools-iuc
    repository to allow a subsequent pull request to fix a problem with bwa.


    \b
        $ planemo clone --branch bwa-fix tools-iuc
        $ cd tools-iuc
        $ # Make changes.
        $ git add -p # Add desired changes.
        $ git commit -m "Fix bwa problem."
        $ planemo pull_request -m "Fix bwa problem."

    These changes do require that a github username and password are
    specified in ~/.planemo.yml.
    """
    if target in CLONE_GITHUB_TARGETS:
        target = "https://github.com/%s" % CLONE_GITHUB_TARGETS[target]
    # Pretty hacky that this path isn't treated as None.
    if path is None or path.endswith("__NONE__"):
        path = target.split("/")[-1]
    github_util.clone_fork_branch(ctx, target, path, **kwds)
