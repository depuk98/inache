import io
import os
import subprocess
import sys
import hashlib


class VirtualEnvironmentError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class VirtualEnvironmentManager:
    def __init__(self, venv_name):
        self.venv_name = venv_name
    def get_venv(self):
        current_directory = os.getcwd()
        print("Current working directory:", current_directory)
        python_path=os.path.join(current_directory, self.venv_name, 'bin', 'python3')
        return python_path
       
    def create_virtual_environment(self):
        self.getCWD()
        if os.path.isdir(self.venv_name):
            print(f'Python virtual environment "{self.venv_name}" exists.')
        else:
            result = subprocess.run(["python3", "-m", "venv", self.venv_name])
            if result.returncode != 0:
                print("Error: Virtual environment creation failed.")
                sys.exit(1)
            print(f'Python virtual environment "{self.venv_name}" created.')

    def activate_virtual_environment(self):
        activate_this = self.venv_name+'/bin/activate_this.py'

        # activate_script_path = os.path.join(self.venv_name, 'bin', 'activate')
        print("the path is ", activate_this)
        with open(activate_this, 'r') as file:
            exec(file.read(), dict(__file__=activate_this))
        # activation_result = subprocess.run(f'source {activate_script_path}', shell=True, executable='/bin/bash')
        # if activation_result.returncode == 0:
        #     print("Virtual environment activation was successful.")
        # else:
        #     print("Error: Virtual environment activation failed.")
        #     sys.exit(1)

    def install_requirements(self):
        print("Checking if the virtual environment is activated:", os.environ.get('VIRTUAL_ENV'))
        venv_pip = os.path.join(self.venv_name, 'bin', 'pip')
        install_result = subprocess.run([venv_pip, "install", "-r", "requirements.txt"])
        if install_result.returncode != 0:
            print("Error: Failed to install requirements.")
            sys.exit(1)  # Exit with code 1 if the requirements installation failed
        print(f'Virtual environment "{self.venv_name}" activated and requirements installed.')
        current_directory = os.getcwd()
        print("Current working directory:", current_directory)

    def getCWD(self):
        current_directory = os.getcwd()
        print("Current working directory:", current_directory)

    def set_environment_variable(self):
        current_directory = os.getcwd()
        print("Current working directory:", current_directory)
        os.environ['DJANGO_SETTINGS_MODULE'] = 'InacheBackend.settings.staging'
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'InacheBackend.settings.staging')
        print(f"DJANGO_SETTINGS_MODULE set to: {os.environ['DJANGO_SETTINGS_MODULE']}")

    def apply_migrations(self):
        python_path = self.get_venv()
        migrate_result = subprocess.run([python_path, "manage.py", "migrate"])
        if migrate_result.returncode == 0:
            print("Migrations applied successfully")
        else:
            print(f"Error: Failed to apply the migrations. Exit code: {migrate_result}")
            sys.exit(1)

    def add_cronjobs(self):
        python_path = self.get_venv()
        crontab_result = subprocess.run([python_path, "manage.py", "crontab", "add"])
        if crontab_result.returncode == 0:
            print("CRONJOBS added successfully")
        else:
            print(f"Error: Failed to add the CRONJOBS. Exit code: {crontab_result}")
            sys.exit(1)

    def collect_static_files(self):
        python_path = self.get_venv()
        subprocess.run([python_path, "manage.py", "collectstatic", "--noinput"])

    def restart_gunicorn_service(self):
        print(f"The current user is : {os.getenv('USER')}")
        service_name = "gunicorn.service"

        print(f"Checking the status of {service_name}")
        status = subprocess.getoutput(f"sudo systemctl status {service_name}")
        print(f"The status of {service_name} is:\n{status}\n")

        print(f"Starting the {service_name}")
        start_result = subprocess.run(["sudo", "systemctl", "restart", "gunicorn.service"]).returncode
        if start_result == 0:
            print(f"{service_name} has been restarted.")
        else:
            print(f"Error: Failed to start {service_name}. Exit code: {start_result.returncode}")
            sys.exit(1)

        print(f"Now again re-checking the status of {service_name} after the restart ")
        status = subprocess.getoutput(f"sudo systemctl status {service_name}")
        print(f"The status of {service_name} after restart:\n{status}\n")
    def celery_restart(self):
        print("Restarting Celery Worker and Beat...")
        python_path = self.get_venv()

        # Stop Celery processes
        # stop_result = subprocess.run(["pkill", "-f", "celery -A InacheBackend"])
        # if stop_result.returncode == 0:
        #     print("Celery processes stopped successfully.")
        # else:
        #     print(f"Error: Failed to stop Celery processes. Exit code: {stop_result.returncode}")
        #     sys.exit(1)

        # Start Celery Worker
        worker_result = subprocess.run([python_path, "manage.py", "celery", "worker", "--detach", "--loglevel=info"])
        if worker_result.returncode == 0:
            print("Celery Worker started successfully.")
        else:
            print(f"Error: Failed to start Celery Worker. Exit code: {worker_result.returncode}")
            sys.exit(1)

        # Start Celery Beat
        beat_result = subprocess.run([python_path, "manage.py", "celery", "beat", "--detach", "--loglevel=info"])
        if beat_result.returncode == 0:
            print("Celery Beat started successfully.")
        else:
            print(f"Error: Failed to start Celery Beat. Exit code: {beat_result.returncode}")
            sys.exit(1)
        

    def hashcheck(self):
        # Calculate the MD5 hash of the requirements.txt file
        with open('requirements.txt', 'rb') as file:
            file_contents = file.read()
        
        md5_hash = hashlib.md5(file_contents)
        md5_hex = md5_hash.hexdigest()
        
        hash_file_path = 'md5_hash.txt'
        
        try:
            with open(hash_file_path, 'r') as hash_file:
                existing_hash = hash_file.read()
        except FileNotFoundError:
            existing_hash = None  # Handle the case where the file doesn't exist yet
            
        print(f"Calculated Hash: {md5_hex}")
        print(f"Existing Hash: {existing_hash}")
        
        if existing_hash != md5_hex:
            # The hashes are not equal, so the requirements.txt file has changed
            with open(hash_file_path, 'w') as hash_file:
                hash_file.write(md5_hex)
            print("Hashes are not equal")
            return False
        else:
            print("Hashes are equal")
            return True

    def main(self):
        try:
            self.getCWD()
            self.create_virtual_environment()
            self.activate_virtual_environment()
            flag=self.hashcheck()
            if flag==False:
                self.install_requirements()
            self.getCWD()
            # self.set_environment_variable()
            self.apply_migrations()
            self.add_cronjobs()
            self.collect_static_files()
            self.celery_restart()
            self.restart_gunicorn_service()
        except VirtualEnvironmentError as e:
            print(f"Error: {e}")
            sys.exit(1)


if __name__ == "__main__":
    if os.environ.get('DJANGO_SETTINGS_MODULE') == 'InacheBackend.settings.staging':
        venv_manager = VirtualEnvironmentManager("stage_environment")
    if os.environ.get('DJANGO_SETTINGS_MODULE') == 'InacheBackend.settings.production':
        venv_manager = VirtualEnvironmentManager("prod_environment")
    
    venv_manager.main()
    
