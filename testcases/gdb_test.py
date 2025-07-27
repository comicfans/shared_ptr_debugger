import click
import run_under_gdb


@click.command()
@click.option("--gdb", help="which gdb to test")
@click.option("--binary", help="which binary to test")
def main(gdb, binary):
    run_under_gdb.run(gdb, binary)


if __name__ == "__main__":
    main()
