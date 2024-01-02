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
@click.option('--output','-o',required=False, help='json output file')
@click.option('--list_id','-li',required=True,help='string list id (comma separated)')
@click.option('--file','-f',is_flag=True, default=False, required=False,help='list provided is a file')
def get_users_info(list_id:str,output:str,file:bool):
    '''Get user info from id list provided'''
    try:
        user = UserSpider()
        user.athlete_info(list_id,output,file)
    except Exception as e:
        click.secho('Need login (use scrapin command first)', fg='red')

@opening.command
@click.option('--output','-o',required=False, help='json output file')
@click.option('--name','-n',required=True,help='Athlete name to search')
def search_user(output:str,name:str):
    '''Search users by name'''
    try:
        user_search = UserSpider()
        user_search.user_search(name,output)
        page = click.prompt('page ("q" to exit)')
        while(page != 'q'):
            user_search.next_page(page)
            page = click.prompt('page')
    except Exception as e:
        click.secho('Need login (use scrapin command first)', fg='red')

if __name__ == '__main__':
    opening()
