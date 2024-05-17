# ruff: noqa: E501

import os
import shutil
import subprocess
import time
from pathlib import Path

# This script builds the software of this repository.
# If it's building the master/main git branch => location on network (network_sw_root) gets updated with this new build

# REMARK: For different SW / OS, change the first variables.

project_path = Path("C:/repos/PandasGUI")
sw_name = "DataViewer"
network_sw_root = Path(
    "//domainserver/SharedDocs/6 - IT/99 - Software/custom_sofics_software"  # network folder that holds up-to-date SW
)

network_sw_root = network_sw_root / "windows" if os.name == "nt" else "linux"  # win/linux build subfolder
network_sw_path = network_sw_root / sw_name

current_branch = subprocess.getoutput("git branch --show-current")
# real build if building master/main git branch
# TODO branch sofics => always real build ? or current_branch == "sofics"
real_build = bool(current_branch == "master" or current_branch == "main" or current_branch == "sofics")

print("Start building " + sw_name)
start = time.time()
# sp.call waits until the subprocess is finished

command_args = ["pyinstaller.exe"] if os.name == "nt" else ["pyinstaller"]
command_args += [
    "--clean",
    "-n",
    f"{sw_name}",
    "--collect-data",
    "qtstylish",
    "--hidden-import",
    "qtstylish.compiled.qtstylish_rc",
    # TODO if multiple problems remain: --collect-submodules qtstylish
    "--add-data",
    "pandasgui/resources;pandasgui/resources",
    "--icon=pandasgui/resources/images/icon.ico",
    "--noconfirm",
]

# TODO get upx to work... way too big otherwise
# subprocess.CalledProcessError: Command '['./scripts/upx\\upx', '--compress-icons=0', '--lzma', '-q', '--strip-loadconf', 'C:\\Users\\rboone\\AppData\\Local\\pyinstaller\\bincache01py31264bit\\_uuid.pyd']' returned non-zero exit status 1.
# upx: C:\Users\rboone\AppData\Local\pyinstaller\bincache01py31264bit\_uuid.pyd: NotCompressibleException
# subprocess.CalledProcessError: Command '['./scripts/upx\\upx', '--compress-icons=0', '--lzma', '-q', '--strip-loadconf', 'C:\\Users\\rboone\\AppData\\Local\\pyinstaller\\bincache01py31264bit\\python3.dll']
# upx: C:\Users\rboone\AppData\Local\pyinstaller\bincache01py31264bit\python3.dll: NotCompressibleException
# TODO subprocess.CalledProcessError: Command '['./scripts/upx\\upx', '--compress-icons=0', '--lzma', '-q', '--strip-loadconf', 'C:\\Users\\rboone\\AppData\\Local\\pyinstaller\\bincache01py31264bit\\api-ms-win-core-file-l2-1-0.dll']' returned non-zero exit status 1.
# TODO upx: C:\Users\rboone\AppData\Local\pyinstaller\bincache01py31264bit\api-ms-win-core-file-l2-1-0.dll: NotCompressibleException
# if real_build:
#     # command_args.append("--windowed")  # Not using this option to avoid SVN pop-ups + show potential exceptions.
#     command_args.append("--upx-dir=./scripts/upx")
#     # TODO check if _greenlet.cp311-win_amd64.pyd is actually problematic
#     command_args.append("--upx-exclude=_greenlet.*.pyd")


command_args.append("main.py")

subprocess.call(command_args, cwd=project_path)  # noqa: s603

end = time.time()
print(f"Build finished, took {round(end - start)}s.\n")

# update SW on network if built from master/main branch
if real_build:
    print("PRODUCTION BUILD:\nupdating " + sw_name + " on the network...")
    start = time.time()

    # copy build to network with "_new" suffix
    network_sw_path_new = Path(str(network_sw_path) + "_new")
    if network_sw_path_new.exists():
        shutil.rmtree(network_sw_path_new)
    shutil.copytree(project_path / "dist" / sw_name, network_sw_path_new)

    # rename old sw on network (add "_old" suffix)
    network_sw_path_old = Path(str(network_sw_path) + "_old")
    if network_sw_path_old.exists():
        shutil.rmtree(network_sw_path_old)
    if not network_sw_path.exists():  # avoid rename exceptions/... if running for the first time ever.
        network_sw_path.mkdir(parents=True)
    network_sw_path.rename(network_sw_path_old)

    # remove "_new" suffix of new software folder => this one is used from now on
    network_sw_path_new.rename(network_sw_path)

    end = time.time()
    print(f"\nSUCCESS:\nbuild was placed on the network, took {round(end - start)}s.\n{network_sw_path}\n")

    # delete old sw ("_old") from network
    print("\nDeleting old version from network...")
    shutil.rmtree(f"{network_sw_path}_old")


# clean up created .spec file and build folder; not used & doesn't create slower build next time.
os.remove(f"{sw_name}.spec")  # noqa: PTH107 no FileNotFoundError; file will always be created
shutil.rmtree("build")  # remove local "build" folder
