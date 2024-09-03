# -*- Coding:utf-8 -*-

"""
################################################################################
run to install the minghu6 python-package;
be independent on minghu6's other content.
################################################################################
"""

from pathlib import Path

DEFAULT_MOD_PARENTDIR = Path(__file__).resolve().parent.parent

def find_valid_site_packages():
    import site

    site_dir = Path(site.getusersitepackages())

    if not site_dir.exists():
        print('User site packages directory isn\'t exist, maybe pyenv?')

        while True:
            match input('Try first site packages directory or continue(t/c):').strip().lower():
                case 't':
                    site_dir = Path(site.getsitepackages()[0])
                    break
                case 'c':
                    site_dir.mkdir(parents=True)
                    break

    return site_dir


def make_pth_file(mod_parentdir = DEFAULT_MOD_PARENTDIR):
    site_dir = find_valid_site_packages()

    pth_path = site_dir.joinpath('minghu6.pth')
    pth_content = mod_parentdir

    print(f'Install {pth_path}:\n{pth_content}')

    with open(pth_path, 'w') as file:
        file.write(f'{pth_content}\n')

    print(f'Install boot requirements...')

    install_mod_requirements([mod_parentdir.joinpath('requirements-boot.txt')])


def install_mod_requirements(req_paths):
    import subprocess

    args_acc = ['pip', 'install']

    for req_path in req_paths:
        args_acc.extend(['-r', str(req_path)])

    cmd = ' '.join(args_acc)

    print(f'Run: {cmd}')

    subprocess.run(cmd, shell=True, check=True)


# import platform
# def islinux():
#     return platform.platform().upper().startswith('LINUX')
# def iswin():
#     return platform.platform().upper().startswith('WIN')


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        make_pth_file(sys.argv[1])
    else:
        make_pth_file()
