import os
import subprocess
import sys
import json
import inquirer

MONOREPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
APPS_DIR = os.path.join(MONOREPO_ROOT, 'apps')

def get_app_info(app_path):
    config_path = os.path.join(app_path, 'launcher_config.json')
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return json.load(f)
    return None

def run_app(app_name, app_path, run_command):
    print(f"\nRunning app: {app_name}")
    print(f"Changing directory to: {app_path}")
    os.chdir(app_path)

    venv_path = os.path.join(app_path, '.venv')
    if not os.path.exists(venv_path):
        print("Virtual environment not found. Creating...")
        subprocess.run([sys.executable, '-m', 'venv', '.venv'], check=True)

    print("Activating virtual environment and installing dependencies...")
    activate_script = os.path.join(venv_path, 'bin', 'activate')
    if sys.platform == "win32":
        activate_script = os.path.join(venv_path, 'Scripts', 'activate')

    # Use a subshell to activate venv and run command
    command = f"source {activate_script} && pip install -r requirements.txt && {run_command}"
    
    # For Windows, the activate script is different and needs to be sourced differently
    if sys.platform == "win32":
        command = f"{activate_script} && pip install -r requirements.txt && {run_command}"

    try:
        subprocess.run(command, shell=True, check=True, cwd=app_path)
    except subprocess.CalledProcessError as e:
        print(f"Error running app {app_name}: {e}")
    finally:
        # Change back to original directory (MONOREPO_ROOT) after running app
        os.chdir(MONOREPO_ROOT)

def main():
    print("Scanning for applications...")
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
                    'run_command': app_info.get('run_command')
                })

    if not available_apps:
        print("No runnable applications found in the 'apps/' directory.")
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
            run_app(selected_app['name'], selected_app['path'], selected_app['run_command'])
        else:
            print(f"Error: No run command defined for {selected_app_name}.")
    else:
        print("No application selected.")

if __name__ == '__main__':
    main()
