#! /home/jatin/iitb/third_sem/cs251/project/env_SPC/bin/python
import click
import rstatus, lstatus, rsync, lsync, set_root, initialise, set_server_ip, user_config, enc_dec
 
@click.group()
def cli():
    pass

@cli.group()
def observe():
    pass

@cli.group()
def server():
    pass


@cli.group()
def en_de():
    pass

@cli.group()
def config():
    pass

@cli.command()
@click.option('--l/--r', default=True)
def status(l):
	if l:
		lstatus.lstatus()
	else:
		rstatus.rstatus()

@cli.command()
def add():
	lsync.lsync()

@cli.command()
def sync():
	rsync.sync()


@observe.command()
@click.argument('path',nargs=1)
def set(path):
	set_root.set(path)

@observe.command()
def show():
	set_root.show()


@cli.command()
def init():
	initialise.initialise()

@cli.command()
def version():
	click.echo('  SPC [version 1.0.4]')


@server.command()
@click.argument('address',nargs=1)
def set(address):
	set_server_ip.set(address)

@server.command()
def show():
	set_server_ip.show()


@config.command()
def edit():
	user_config.edit()

@config.command()
def show():
	user_config.show()

@en_de.command()
def list():
	enc_dec.list()

@en_de.command()
def update():
	enc_dec.update()

@en_de.command()
def dump():
	enc_dec.dump()

if __name__ == '__main__':
    cli()