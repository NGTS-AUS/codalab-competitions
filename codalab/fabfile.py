import os
import sys
import warnings
import yaml

from fabric import network
from fabric.api import env, hide, local, quiet, run, warn_only, sudo
from fabric.colors import red, green
from fabric.state import connections

from django.core.exceptions import ImproperlyConfigured

env.setdefault("DJANGO_CONFIGURATION", "Dev")
from django.conf import settings as django_settings
try:
    from codalab.settings import Dev
    django_settings.configure(Dev)
except ImproperlyConfigured, e:
    print 'ERROR: Configuration issue:'
    print '\t', e
    print ''


CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

# Ignore annoying internal fabric depreciated stuff
warnings.filterwarnings("ignore", category=DeprecationWarning)


###############################################################################
# Helpers
def _print(str):
    sys.stdout.write(str)
    sys.stdout.flush()


###############################################################################
# DevOps
def hosts(key):
    """Loads hosts from server_config.yaml in the format of:
            host_key:
              hosts:
                - hostname1
                - hostname2
        """
    assert os.path.exists('server_config.yaml'), "server_config.yaml does not exist next to fabfile.py"
    hosts = yaml.load(open('server_config.yaml').read())
    env.hosts = hosts[key]['hosts']


def compute_worker_init(BROKER_URL, BROKER_USE_SSL=False):
    """Initializes compute worker by installing docker and the compute worker image

    Meant to be used with `hosts` like so:
        fab hosts:prod_workers compute_worker_initialize:url,True
    """
    # Get proper SSL flag value
    BROKER_USE_SSL = bool(BROKER_USE_SSL)

    # Make .env file settings for worker
    env_file = 'BROKER_URL={}'.format(BROKER_URL)
    if BROKER_USE_SSL:
        env_file += "\nBROKER_USE_SSL=True"
    run('echo "{}" > .env'.format(env_file))

    # Install docker
    run('curl https://get.docker.com | sudo sh')

    # Add user to group and reset user group settings so we can run docker without sudo
    user = str(run("echo $USER"))  # we have to get the user name this way...
    sudo('usermod -aG docker {}'.format(user))


def compute_worker_update():
    """Updates compute workers to latest docker image

    Meant to be used with `hosts` like so:
        fab hosts:prod_workers compute_worker_update
    """
    compute_worker_kill()
    run('docker pull ckcollab/competitions-v1-compute-worker:latest')
    run('docker pull {}'.format(django_settings.DOCKER_DEFAULT_WORKER_IMAGE))
    compute_worker_run()


def compute_worker_kill():
    """Kills compute worker

    Meant to be used with `hosts` like so:
        fab hosts:prod_workers compute_worker_kill
    """
    with warn_only():
        # Error if compute_worker isn't already running
        run('docker kill $(docker ps -a -q)')
        run('docker rm $(docker ps -a -q)')


def compute_worker_restart():
    """Restarts compute worker

    Meant to be used with `hosts` like so:
        fab hosts:prod_workers compute_worker_restart
    """
    compute_worker_kill()
    compute_worker_run()


def compute_worker_run():
    """Runs the actual compute worker.

    Meant to be used with `hosts` like so:
        fab hosts:prod_workers compute_worker_run
    """
    run("docker run "
        "--env-file .env "
        "-v /var/run/docker.sock:/var/run/docker.sock "
        "-v /tmp/codalab:/tmp/codalab "
        "-d --restart unless-stopped "
        "--name compute_worker -- "
        "ckcollab/competitions-v1-compute-worker:latest")


def compute_worker_status():
    """Prints out `docker ps` for each worker

    Meant to be used with `hosts` like so:
        fab hosts:prod_workers compute_worker_status
    """
    run('docker ps')


###############################################################################
# Tests
###############################################################################
def test_e2e():
    with hide('running', 'stdout', 'stderr', 'warnings', 'aborts'):
        _print("Running Selenium tests...")
        # insert selenium tests when we get them
        print green("done")


def test_django():
    with hide('running', 'stdout', 'stderr', 'warnings', 'aborts'):
        _print("Running Django tests...")
        local('python manage.py test --noinput', capture=True)
        print green("done")


# def test_lint():
#     with hide('running', 'stdout', 'stderr', 'warnings', 'aborts'):
#         _print("Checking syntax...")
#         local(
#             'flake8 . --max-line-length=120 --exclude=*/migrations/* --ignore=E712,E127,F403,E128,E126,E711,E501',
#             capture=True
#         )
#         print "done"


def test():
    print "%" * 80
    print " Running all tests..."
    print "%" * 80
    print ""

    #test_lint()
    test_django()
    test_e2e()


###############################################################################
# Environment/database
###############################################################################
def fresh_db():
    raise NotImplementedError()
