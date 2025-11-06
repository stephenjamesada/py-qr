import qrcode
import time
from pathlib import Path
from loguru import logger
from platformdirs import user_config_dir
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.table import Table
from rich import print, box
from rich_menu import Menu
from pyfiglet import Figlet, FigletFont

def title():
    fig = Figlet(font="ansi_shadow")
    title = fig.renderText("Py-QR")

    print(Panel.fit(f"[bold cyan]{title}[/bold cyan]\n",
    box=box.SQUARE_DOUBLE_HEAD,
    subtitle="[cyan]Fast, efficient QR codes[/cyan]"))
    time.sleep(2)

    print(Panel.fit("[dim]Made by [link=https://github.com/stephenjamesada]github.com/stephenjamesada[/dim]     ",
    box=box.SQUARE_DOUBLE_HEAD))
    time.sleep(2)

def main():
    while True:
        try:
            # Config and log folders
            config_dir = Path.home() / ".config" / "py-qr"
            config_dir.mkdir(parents=True, exist_ok=True)
            log_dir = Path.home() / ".config" / "py-qr" / "logs"
            log_dir.mkdir(parents=True, exist_ok=True)

            logger.remove()

            logger.add(log_dir / "py-qr.log", rotation="1 MB", compression="zip")

            logger.info("App started.")

            data = Prompt.ask("[cyan]Enter your text (enter q to quit, d for details)[/cyan]")

            if data.lower() == 'q':
                print("[green]Goodbye![/green]\n")
                logger.info("Exit app w/ 'q'")
                break
            elif data.lower() == 'd':
                print(Panel.fit("[bold]Version - size & capacity\nBorder - Amount of empty space\nBox size - size of the box[/bold]",
                                box=box.SQUARE_DOUBLE_HEAD,
                                subtitle="[cyan]Details[/cyan]"))
                continue

            version = int(Prompt.ask("[cyan]Enter version (default 1)[/cyan]", default=1))

            if version < 1 or version > 40:
                print("[red]Please use a version between 1 and 40.[/red]\n")
                logger.error("User attempted to use a version that was either less than 1 or higher than 40.")
                continue

            box_size = int(Prompt.ask("[cyan]Enter box size (default 10)[/cyan]", default=10))
            border = int(Prompt.ask("[cyan]Enter border (default 4)[/cyan]", default=4))
            foreground = Prompt.ask("[cyan]Enter foreground[/cyan]", default="black")
            background = Prompt.ask("[cyan]Enter background[/cyan]", default="white")
            code_name = Prompt.ask("[cyan]Name your QR code[/cyan]", default="qr_code")

            file_path = config_dir / f"{code_name}.png"

            qr = qrcode.QRCode(
            version=version,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=box_size,
            border=border
            )

            qr.add_data(data)
            qr.make(fit=True)

            img = qr.make_image(fill_color=foreground, back_color=background)
            img.save(file_path)

            # Setting Table
            console = Console()
            table = Table(box=box.ROUNDED)

            table.add_column("Setting", style="bold cyan")
            table.add_column("Value", style="bold magenta")

            table.add_row("Version", str(version))
            table.add_row("Box Size", str(box_size))
            table.add_row("Border", str(border))

            console.print(table)

            print(f"[bold green]{code_name}.png created at {file_path}[/bold green]")
            logger.debug("QR code image generated w/ version={} box_size={} border={}", version, box_size, border)
        except KeyboardInterrupt:
            print("\n[green]Goodbye![/green]\n")
            logger.info("App terminated by KeyboardInterrupt.")
            break

if __name__ == "__main__":
    title()
    main()
