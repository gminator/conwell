from django.core.management.base import BaseCommand, CommandError
from game.models import Grid
class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('-l', '-length', type=int, help="Grid Length")
        parser.add_argument('-w', '-width', type=int, help="Grid width")
        parser.add_argument('-c', '-initial-cells', type=int, help="Number of cell to randomly populate at start")
        parser.add_argument('-g', '-generations', type=int, help="Generate to iterate through")
        parser.add_argument('-p', '-points',nargs='+', type=str, help="Manually highlight points")

    def handle(self, *args, **options):
        grid = Grid(options["l"],options["w"], options["g"], options['p'],options["c"])
       