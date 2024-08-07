import sys
import json
import os

PACKAGE_LIST_FILE = 'packages.json'

def load_package_list():
    if not os.path.exists(PACKAGE_LIST_FILE):
        print(f"Error: {PACKAGE_LIST_FILE} not found.")
        sys.exit(1)
    with open(PACKAGE_LIST_FILE, 'r') as file:
        return json.load(file)

def install_package(package_name):
    package_data = load_package_list()
    packages = package_data.get('packages', [])

    for pkg in packages:
        if pkg['pkgname'] == package_name:
            print(f"Package Name: {pkg['pkgname']}")
            print(f"Version: {pkg['pkgver']}")
            print(f"Description: {pkg['pkgdesc']}")
            print(f"Dependencies: {pkg['pkgdeps']}")
            
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
            return

    print(f"Package '{package_name}' not found in the package list.")

def main():
    if len(sys.argv) != 3 or sys.argv[1] != 'install':
        print("Usage: pet install [pkgname]")
        sys.exit(1)

    package_name = sys.argv[2]
    install_package(package_name)

if __name__ == "__main__":
    main()
