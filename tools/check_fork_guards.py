import yaml
import sys
import os

def check_guards(directory="."):
    wasmlib_path = os.path.join(directory, ".github", "workflows", "wasmlib.yml")
    python_path = os.path.join(directory, ".github", "workflows", "python.yml")
    cd_path = os.path.join(directory, ".github", "workflows", "cd.yml")

    missing_guards = []

    # 1. wasmlib.yml -> jobs -> publish-wasmlib -> if
    with open(wasmlib_path, 'r') as f:
        wasmlib = yaml.safe_load(f)
        try:
            val = wasmlib['jobs']['publish-wasmlib']['if']
            print(f".github/workflows/wasmlib.yml: jobs.publish-wasmlib.if = {val!r}")
            if val != "github.repository == 'solvespace/solvespace'":
                missing_guards.append("wasmlib.yml publish-wasmlib if")
        except KeyError:
            missing_guards.append("wasmlib.yml publish-wasmlib if")
            print(".github/workflows/wasmlib.yml: jobs.publish-wasmlib.if = MISSING")

    # 2. python.yml -> jobs -> publish-pypi -> if
    with open(python_path, 'r') as f:
        python = yaml.safe_load(f)
        try:
            val = python['jobs']['publish-pypi']['if']
            print(f".github/workflows/python.yml: jobs.publish-pypi.if = {val!r}")
            if val != "github.repository == 'solvespace/solvespace'":
                missing_guards.append("python.yml publish-pypi if")
        except KeyError:
            missing_guards.append("python.yml publish-pypi if")
            print(".github/workflows/python.yml: jobs.publish-pypi.if = MISSING")

    # 3. cd.yml -> jobs -> upload_release_assets -> if
    with open(cd_path, 'r') as f:
        cd = yaml.safe_load(f)
        try:
            val = cd['jobs']['upload_release_assets']['if']
            print(f".github/workflows/cd.yml: jobs.upload_release_assets.if = {val!r}")
            if val != "!cancelled() && github.event_name == 'release' && github.repository == 'solvespace/solvespace'":
                missing_guards.append("cd.yml upload_release_assets if")
        except KeyError:
            missing_guards.append("cd.yml upload_release_assets if")
            print(".github/workflows/cd.yml: jobs.upload_release_assets.if = MISSING")

    # 4. cd.yml -> jobs -> build_release_macos -> steps -> Sign Build -> if
    try:
        steps = cd['jobs']['build_release_macos']['steps']
        sign_step = next(s for s in steps if s.get('name') == 'Sign Build')
        val = sign_step['if']
        print(f".github/workflows/cd.yml: jobs.build_release_macos.steps['Sign Build'].if = {val!r}")
        if val != "github.repository == 'solvespace/solvespace'":
            missing_guards.append("cd.yml build_release_macos Sign Build if")
    except (KeyError, StopIteration):
        missing_guards.append("cd.yml build_release_macos Sign Build if")
        print(".github/workflows/cd.yml: jobs.build_release_macos.steps['Sign Build'].if = MISSING")

    # 5. cd.yml -> jobs -> build_release_web -> steps -> Ping solvespace.com -> if
    try:
        steps = cd['jobs']['build_release_web']['steps']
        ping_step = next(s for s in steps if s.get('name') == 'Ping solvespace.com')
        val = ping_step['if']
        print(f".github/workflows/cd.yml: jobs.build_release_web.steps['Ping solvespace.com'].if = {val!r}")
        if val != "github.repository == 'solvespace/solvespace'":
            missing_guards.append("cd.yml build_release_web Ping solvespace.com if")
    except (KeyError, StopIteration):
        missing_guards.append("cd.yml build_release_web Ping solvespace.com if")
        print(".github/workflows/cd.yml: jobs.build_release_web.steps['Ping solvespace.com'].if = MISSING")

    if missing_guards:
        print("MISSING OR INCORRECT GUARDS:", missing_guards)
        sys.exit(1)
    else:
        print("ALL GUARDS PRESENT AND CORRECT")

if __name__ == '__main__':
    directory = sys.argv[1] if len(sys.argv) > 1 else "."
    check_guards(directory)
