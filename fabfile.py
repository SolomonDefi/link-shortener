# pylint: skip-file
from fabric import Connection, Config
from invoke import task, run
from datetime import datetime
import os


class BaseConfig(object):
    DO_DB = False
    FOLDER = '/home/solomondefi/shortener'
    SERVICE = 'shortener'
    BACKUP = True
    HOST = os.environ.get('SLM_SHORTENER_HOST', None)
    PASSWORD = os.environ.get('SLM_SHORTENER_PASSWORD', None)
    ENV = 'prod'

    @property
    def ENV_FILE(self):
        return f'{self.ENV}.env'


@task
def deploy(c):
    config = BaseConfig()
    conn = setup(config)
    venv_folder = '.venv'
    if not conn:
        return
    f = config.FOLDER

    conn.sudo(f'service {config.SERVICE} stop')
    with conn.cd(f):
        backup_name = datetime.now().strftime('%y%m%d_%H%M%S')
        backup_file = f'../backups/{backup_name}.db'
        conn.run(
            f'mkdir -p ../backups && [[ -e app.db ]] && cp app.db {backup_file}',
            warn=True,
        )

    run(
        f'rsync -az --force --delete --progress --exclude-from=rsync_exclude.txt -e "ssh -p22" ./ {config.HOST}:{f}'
    )
    with conn.cd(f):
        conn.run(f'cp ./env/{config.ENV_FILE} ./.env')
        conn.run(f'rm -rf {venv_folder}')
        conn.run(f'/home/solomondefi/.local/bin/virtualenv -p python3 {venv_folder}')
        conn.run(f'source {venv_folder}/bin/activate && poetry install')
        conn.run(f'source {venv_folder}/bin/activate && poetry run flask db upgrade')
    conn.sudo(f'service {config.SERVICE} start')


def setup(config):
    if not config.HOST:
        print("HOST env var not set")
        return None

    overrides = {'sudo': {'password': config.PASSWORD}} if config.PASSWORD else {}
    fab_config = Config(overrides=overrides)
    print(f'Using host {config.HOST}')
    return Connection(config.HOST, config=fab_config)
