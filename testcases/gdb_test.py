import click
import run_under_gdb


@click.command()
@click.option("--gdb", help="which gdb to test")
@click.option("--init", help="where to load gdb init")
@click.option("--binary", help="which binary to test")
def main(gdb, init, binary):
    run_under_gdb.run(gdb, init, binary)


if __name__ == "__main__":
    main()
