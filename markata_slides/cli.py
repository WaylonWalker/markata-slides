from markata import Markata
from markata.hookspec import hook_impl


def run():
    m = Markata()
    m._pm.register('markata_slides')
    if "prevnext" not in str(m.hooks):
        m._pm.register('markata.plugins.prevnext')
    m.configure()
    m.run()

@hook_impl()
def cli(app, markata: Markata) -> None:
    @app.command()
    def slides() -> None:
        run()
