"""
Custom setup for Flask's CLI runner
"""
import click
from flask_migrate import Migrate
from application import create_app

app = create_app()
migrate = Migrate(app, app.db)


@app.cli.command()
@click.option(
    '-x', 'stop', flag_value='-x', default=False, help='Stop tests on the first failure'
)
def test(**args):
    from tests.conftest import run_tests

    run_tests([arg for arg in args.values() if arg])


@app.cli.command()
def lint():
    import pylint.lint

    pylint.lint.Run(
        [
            '--load-plugins',
            'pylint_flask',
            'application.py',
            'fabfile.py',
            'cli_setup.py',
            'wsgi.py',
            'shortener',
            'tests',
        ]
    )


@app.cli.command()
def formatter():
    """
    Use `black` to format the code
    """
    import black
    from click.testing import CliRunner
    from pathlib import Path

    code_root = Path(__file__).parent
    runner = CliRunner()
    result = runner.invoke(
        black.main,
        [
            str(code_root / target)
            for target in [
                'application.py',
                'fabfile.py',
                'wsgi.py',
                'shortener',
                'cli_setup.py',
                'tests',
            ]
        ]
        + ['--skip-string-normalization'],
    )
    assert result.exit_code == 0, result.output
