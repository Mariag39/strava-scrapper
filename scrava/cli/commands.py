import click
from pyfiglet import Figlet
import sys
from scrava.core import StravaSpider
from scrava.users import UserSpider


@click.group
def opening():
    custom_fig = Figlet(font='rectangles')
    click.secho('   ***************************************', fg='blue')
    click.secho(custom_fig.renderText('SCRava'))
    click.secho('   ***************************************', fg='blue')
    click.secho('   Strava scraper\n   by: Maria Raldu\n', fg='red')

@opening.command
def scrapin():
    '''Strava Login'''
    log = StravaSpider()
    try:
        email = click.prompt('email')
        password = click.prompt('password')
        log.login(email, password)
    except Exception as e:
        print(e)

@opening.command
def get_users_info():
    '''Get user info from id list provided'''
    user = UserSpider()
    user.athlete_info('56868533')


if __name__ == '__main__':
    opening()
