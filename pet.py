import sys
import json
import os
import requests

PACKAGE_LIST_FILE = 'packages.json'
REPOSITORIES_DIR = 'repositories'

def load_package_list(repo_dir=None):
    if repo_dir is None:
        package_file_path = PACKAGE_LIST_FILE
    else:
        package_file_path = os.path.join(repo_dir, 'packages.json')
    
    if not os.path.exists(package_file_path):
        print(f"Error: {package_file_path} not found.")
        sys.exit(1)
    
    with open(package_file_path, 'r') as file:
        return json.load(file)

def save_package_list(package_data):
    with open(PACKAGE_LIST_FILE, 'w') as file:
        json.dump(package_data, file, indent=4)

def install_package(package_name):
    repo_dirs = [d for d in os.listdir(REPOSITORIES_DIR) if os.path.isdir(os.path.join(REPOSITORIES_DIR, d))]
    
    found = False
    for repo_name in repo_dirs:
        repo_path = os.path.join(REPOSITORIES_DIR, repo_name)
        try:
            package_data = load_package_list(repo_path)
            packages = package_data.get('packages', [])

            for pkg in packages:
                if pkg['pkgname'] == package_name:
                    print(f"Package Name: {pkg['pkgname']}")
                    print(f"Version: {pkg['pkgver']}")
                    print(f"Description: {pkg['pkgdesc']}")
                    print(f"Dependencies: {pkg['pkgdeps']}")
                    print(f"Source Repository: {repo_name}")

                    if pkg['pkgdeps'] and package_name == 'petpet-base':
                        dependencies = pkg['pkgdeps'].split()
                        print(f"\nThis package installs the following dependencies:")
                        print(f"{', '.join(dependencies)}")

                        confirmation = input(f"\nDo you want to install '{package_name}' and its dependencies? (Y/N): ").strip().upper()

                        if confirmation == 'Y':
                            print(f"\nInstalling '{package_name}' and dependencies...")
                            for dep in dependencies:
                                print(f"Installing {dep}...")
                            print(f"Package '{package_name}' and dependencies installed successfully.")
                        elif confirmation == 'N':
                            print(f"\nInstallation of '{package_name}' and dependencies cancelled.")
                        else:
                            print(f"\nInvalid input. Please enter 'Y' or 'N'.")
                    else:
                        confirmation = input(f"\nDo you want to install '{package_name}'? (Y/N): ").strip().upper()

                        if confirmation == 'Y':
                            print(f"\nInstalling '{package_name}'...")
                            print(f"Package '{package_name}' installed successfully.")
                        elif confirmation == 'N':
                            print(f"\nInstallation of '{package_name}' cancelled.")
                        else:
                            print(f"\nInvalid input. Please enter 'Y' or 'N'.")
                    
                    found = True
                    return

        except json.JSONDecodeError:
            print(f"Error decoding JSON in repository '{repo_name}'.")
    
    if not found:
        print(f"Package '{package_name}' not found in any repository.")

def remove_package(package_name):
    installed_dir = 'installed'
    if not os.path.exists(installed_dir):
        print(f"Error: No packages are currently installed.")
        return

    installed_packages = [pkg for pkg in os.listdir(installed_dir) if os.path.isdir(os.path.join(installed_dir, pkg))]
    
    if package_name not in installed_packages:
        print(f"Package '{package_name}' is not installed on the system.")
        return

    confirmation = input(f"\nDo you want to remove '{package_name}'? (Y/N): ").strip().upper()
    
    if confirmation == 'Y':
        package_dir = os.path.join(installed_dir, package_name)
        if os.path.exists(package_dir):
            os.rmdir(package_dir)
        print(f"\nPackage '{package_name}' removed successfully.")
    elif confirmation == 'N':
        print(f"\nRemoval of '{package_name}' cancelled.")
    else:
        print(f"\nInvalid input. Please enter 'Y' or 'N'.")

def update_package(package_name):
    package_data = load_package_list()
    packages = package_data.get('packages', [])
    
    for pkg in packages:
        if pkg['pkgname'] == package_name:
            print(f"Updating '{package_name}'...")
            print(f"Package '{package_name}' updated successfully.")
            return

    print(f"Package '{package_name}' not found in the package list.")

def update_all():
    package_data = load_package_list()
    packages = package_data.get('packages', [])
    
    print("Updating all packages...")
    for pkg in packages:
        print(f"Updating '{pkg['pkgname']}'...")
    print("All packages updated successfully.")

def add_repo(repo_url):
    try:
        response = requests.get(repo_url)
        response.raise_for_status()

        repo_data = response.json()
        repo_name = repo_data.get('repositoryName')

        if not repo_name:
            print("Repository JSON does not contain 'repositoryName'.")
            return

        repo_dir = os.path.join(REPOSITORIES_DIR, repo_name)
        os.makedirs(repo_dir, exist_ok=True)

        packages_file_path = os.path.join(repo_dir, 'packages.json')
        with open(packages_file_path, 'w') as file:
            json.dump(repo_data, file, indent=4)

        print(f"Repository '{repo_name}' added successfully.")

    except requests.RequestException as e:
        print(f"Error fetching repository: {e}")
    except json.JSONDecodeError:
        print("Error decoding JSON from the repository URL.")

def find_package(package_name):
    if not os.path.exists(REPOSITORIES_DIR):
        print(f"Error: No repositories found.")
        return

    repo_dirs = [d for d in os.listdir(REPOSITORIES_DIR) if os.path.isdir(os.path.join(REPOSITORIES_DIR, d))]
    found = False

    for repo_name in repo_dirs:
        repo_path = os.path.join(REPOSITORIES_DIR, repo_name)
        packages_json_path = os.path.join(repo_path, 'packages.json')
        
        if os.path.isfile(packages_json_path):
            with open(packages_json_path, 'r') as file:
                try:
                    repo_data = json.load(file)
                    packages = repo_data.get('packages', [])
                    for pkg in packages:
                        if pkg['pkgname'] == package_name:
                            print(f"Package '{package_name}' found in repository '{repo_name}'.")
                            found = True
                            break
                except json.JSONDecodeError:
                    print(f"Error decoding JSON in repository '{repo_name}'.")

        if found:
            break

    if not found:
        print(f"Package '{package_name}' not found in any repository.")

def main():
    if len(sys.argv) < 2:
        print("Usage: pet [install|remove|update|add-repo|find] [pkgname|all|repo-url]")
        sys.exit(1)

    command = sys.argv[1]

    if command == 'install':
        if len(sys.argv) != 3:
            print("Usage: pet install [pkgname]")
            sys.exit(1)
        package_name = sys.argv[2]
        install_package(package_name)
    
    elif command == 'remove':
        if len(sys.argv) != 3:
            print("Usage: pet remove [pkgname]")
            sys.exit(1)
        package_name = sys.argv[2]
        remove_package(package_name)
    
    elif command == 'update':
        if len(sys.argv) == 3 and sys.argv[2] == 'all':
            update_all()
        elif len(sys.argv) == 3:
            package_name = sys.argv[2]
            update_package(package_name)
        else:
            print("Usage: pet update [pkgname|all]")
            sys.exit(1)
    
    elif command == 'add-repo':
        if len(sys.argv) != 3:
            print("Usage: pet add-repo [repo-url]")
            sys.exit(1)
        repo_url = sys.argv[2]
        add_repo(repo_url)
    
    elif command == 'find':
        if len(sys.argv) != 3:
            print("Usage: pet find [pkgname]")
            sys.exit(1)
        package_name = sys.argv[2]
        find_package(package_name)

    else:
        print("Usage: pet [install|remove|update|add-repo|find] [pkgname|all|repo-url]")
        sys.exit(1)

if __name__ == "__main__":
    main()
