import os
import subprocess
import sys
import json
import inquirer
from rich.console import Console

console = Console()

MONOREPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
APPS_DIR = os.path.join(MONOREPO_ROOT, 'apps')

def get_app_info(app_path):
    config_path = os.path.join(app_path, 'launcher_config.json')
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return json.load(f)
    return None

def run_app(app_name, app_path, run_command, shared_libs=None):
    console.print(f"\n[bold green]Running app:[/bold green] [cyan]{app_name}[/cyan]")
    console.print(f"[bold green]Changing directory to:[/bold green] [yellow]{app_path}[/yellow]")
    os.chdir(app_path)

    venv_path = os.path.join(app_path, '.venv')
    if not os.path.exists(venv_path):
        console.print("[bold yellow]Virtual environment not found. Creating...[/bold yellow]")
        subprocess.run([sys.executable, '-m', 'venv', '.venv'], check=True)

    console.print("[bold green]Activating virtual environment and installing dependencies...[/bold green]")
    activate_script = os.path.join(venv_path, 'bin', 'activate')
    if sys.platform == "win32":
        activate_script = os.path.join(venv_path, 'Scripts', 'activate')

    # Construct PYTHONPATH for shared libraries and app's src directory
    pythonpath_env = os.environ.copy()
    pythonpath_entries = [os.path.join(app_path, 'src')]
    if shared_libs:
        for lib_name in shared_libs:
            lib_src_path = os.path.join(MONOREPO_ROOT, 'libs', lib_name, 'src')
            if os.path.exists(lib_src_path):
                pythonpath_entries.append(lib_src_path)
    
    # Add existing PYTHONPATH to the end
    current_pythonpath = pythonpath_env.get('PYTHONPATH', '')
    if current_pythonpath:
        pythonpath_entries.append(current_pythonpath)

    pythonpath_env['PYTHONPATH'] = os.pathsep.join(pythonpath_entries)

    # Use a subshell to activate venv and run command
    command = f"source \"{activate_script}\" && pip install -r requirements.txt && {run_command}"
    
    # For Windows, the activate script is different and needs to be sourced differently
    if sys.platform == "win32":
        command = f"\"{activate_script}\" && pip install -r requirements.txt && {run_command}"

    try:
        # Setup environment for specific apps
        if app_name == "file_butler":
            console.print("[bold yellow]Setting up dummy directory for file_butler...[/bold yellow]")
            subprocess.run(["mkdir", "-p", "/tmp/test_files_for_file_butler"], check=True)
        elif app_name == "image_optimizer":
            console.print("[bold yellow]Setting up dummy directories and image for image_optimizer...[/bold yellow]")
            subprocess.run(["mkdir", "-p", "/tmp/input_images_for_optimizer"], check=True)
            subprocess.run(["mkdir", "-p", "/tmp/output_images_for_optimizer"], check=True)
            try:
                from PIL import Image
                img = Image.new('RGB', (1920, 1080), color = 'red')
                img.save('/tmp/input_images_for_optimizer/dummy_large.png')
                console.print("[green]Dummy image created.[/green]")
            except ImportError:
                console.print("[bold red]Pillow not found. Cannot create dummy image for image_optimizer.[/bold red]")
            except Exception as e:
                console.print(f"[bold red]Error creating dummy image: {e}[/bold red]")

        subprocess.run(command, shell=True, check=True, cwd=app_path, env=pythonpath_env)
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]Error running app {app_name}: {e}[/bold red]")
    finally:
        # Change back to original directory (MONOREPO_ROOT) after running app
        os.chdir(MONOREPO_ROOT)

def main():
    console.print("[bold blue]Scanning for applications...[/bold blue]")
    available_apps = []
    for app_name in os.listdir(APPS_DIR):
        app_path = os.path.join(APPS_DIR, app_name)
        if os.path.isdir(app_path) and app_name != "cli_launcher": # Exclude the launcher itself
            app_info = get_app_info(app_path)
            if app_info:
                available_apps.append({
                    'name': app_name,
                    'path': app_path,
                    'description': app_info.get('description', 'No description provided.'),
                    'run_command': app_info.get('run_command'),
                    'shared_libs': app_info.get('shared_libs', [])
                })

    if not available_apps:
        console.print("[bold red]No runnable applications found in the 'apps/' directory.[/bold red]")
        return

    choices = [(f"{app['name']} - {app['description']}", app['name']) for app in available_apps]
    questions = [
        inquirer.List(
            'selected_app',
            message="Which application would you like to run?",
            choices=choices,
        ),
    ]

    answers = inquirer.prompt(questions)

    if answers and 'selected_app' in answers:
        selected_app_name = answers['selected_app']
        selected_app = next((app for app in available_apps if app['name'] == selected_app_name), None)

        if selected_app and selected_app['run_command']:
            run_app(selected_app['name'], selected_app['path'], selected_app['run_command'], selected_app['shared_libs'])
        else:
            console.print(f"[bold red]Error: No run command defined for {selected_app_name}.[/bold red]")
    else:
        console.print("[bold red]No application selected.[/bold red]")

if __name__ == '__main__':
    main()
