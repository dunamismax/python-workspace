# apps/cli_launcher/src/cli_launcher/main.py

import json
import os
import subprocess
import sys

import inquirer
from rich.console import Console

console = Console()


class CliLauncher:
    """A class for discovering and running applications in the monorepo."""

    def __init__(self):
        self.monorepo_root = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "..", "..")
        )
        self.apps_dir = os.path.join(self.monorepo_root, "apps")

    def discover_apps(self):
        """Discovers runnable applications in the 'apps' directory."""
        available_apps = []
        for app_name in os.listdir(self.apps_dir):
            app_path = os.path.join(self.apps_dir, app_name)
            if os.path.isdir(app_path) and app_name != "cli_launcher":
                config_path = os.path.join(app_path, "launcher_config.json")
                if os.path.exists(config_path):
                    with open(config_path, "r") as f:
                        app_info = json.load(f)
                        available_apps.append({
                            "name": app_name,
                            "path": app_path,
                            "description": app_info.get("description", "No description provided."),
                            "run_command": app_info.get("run_command"),
                            "shared_libs": app_info.get("shared_libs", []),
                        })
        return available_apps

    def run_app(self, app):
        """Runs the selected application."""
        console.print(f"\n[bold green]Running app:[/bold green] [cyan]{app['name']}[/cyan]")
        os.chdir(app["path"])

        self._setup_venv(app["path"])
        self._run_command(app)

    def _setup_venv(self, app_path):
        """Sets up the virtual environment for the application."""
        venv_path = os.path.join(app_path, ".venv")
        if not os.path.exists(venv_path):
            console.print("[bold yellow]Virtual environment not found. Creating...[/bold yellow]")
            subprocess.run([sys.executable, "-m", "venv", ".venv"], check=True)

    def _run_command(self, app):
        """Runs the application's command with the correct PYTHONPATH."""
        pythonpath = self._get_pythonpath(app)
        env = os.environ.copy()
        env["PYTHONPATH"] = pythonpath

        command = self._get_command(app)

        try:
            subprocess.run(command, shell=True, check=True, cwd=app["path"], env=env)
        except subprocess.CalledProcessError as e:
            console.print(f"[bold red]Error running app {app['name']}: {e}[/bold red]")
        finally:
            os.chdir(self.monorepo_root)

    def _get_pythonpath(self, app):
        """Constructs the PYTHONPATH for the application."""
        paths = [os.path.join(app["path"], "src")]
        if app.get("shared_libs"):
            for lib_name in app["shared_libs"]:
                lib_src_path = os.path.join(self.monorepo_root, "libs", lib_name, "src")
                if os.path.exists(lib_src_path):
                    paths.append(lib_src_path)

        current_pythonpath = os.environ.get("PYTHONPATH", "")
        if current_pythonpath:
            paths.append(current_pythonpath)

        return os.pathsep.join(paths)

    def _get_command(self, app):
        """Constructs the command to run the application."""
        activate_script = os.path.join(app["path"], ".venv", "bin", "activate")
        if sys.platform == "win32":
            activate_script = os.path.join(app["path"], ".venv", "Scripts", "activate")

        return (
            f'source "{activate_script}" && pip install -r requirements.txt && {app["run_command"]}'
        )

    def main(self):
        """The main entry point for the CLI launcher."""
        console.print("[bold blue]Welcome to the Python Monorepo CLI Launcher![/bold blue]")
        available_apps = self.discover_apps()

        if not available_apps:
            console.print("[bold red]No runnable applications found.[/bold red]")
            return

        choices = [(f"{app['name']} - {app['description']}", app) for app in available_apps]
        questions = [
            inquirer.List(
                "selected_app",
                message="Which application would you like to run?",
                choices=choices,
            ),
        ]

        answers = inquirer.prompt(questions)

        if answers and "selected_app" in answers:
            self.run_app(answers["selected_app"])
        else:
            console.print("[bold red]No application selected.[/bold red]")


if __name__ == "__main__":
    launcher = CliLauncher()
    launcher.main()
