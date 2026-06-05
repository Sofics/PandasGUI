import os
import shutil
import subprocess
import time
import zipfile
from pathlib import Path

# This script builds the software of this repository.
# If it's building the master/main git branch => location on network (network_sw_root) gets updated with this new build

# REMARK: For different SW / OS, change the first variables.

project_path = Path(r"C:/repos/PandasGUI")
project_src_path = project_path / "src"
sw_name = "DataViewer"
network_sw_root = Path(
    "//domainserver/softwareupdates"  # network folder that holds up-to-date SW
)

network_sw_root = network_sw_root / "windows" if os.name == "nt" else "linux"  # win/linux build subfolder
network_sw_zip = network_sw_root / f"{sw_name}.zip"

current_branch = subprocess.getoutput("git branch --show-current")
# real build if building master/main git branch
real_build = bool(current_branch == "master" or current_branch == "main")

print(f"\nSTART BUILDING {sw_name} ...")
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
    "--exclude-module",  # make sure to exclude the modules needed only for development
    "pyinstaller",
    "--exclude-module",
    "ruff",
    "--exclude-module",
    "black",
]

real_build = True  # No main branch for now
if real_build:
    # command_args.append("--windowed")  # Not using this option to avoid SVN pop-ups + show potential exceptions.
    command_args.append("--upx-dir=./scripts/upx")
    command_args.append("--upx-exclude=_greenlet.*.pyd")
    command_args.append("--upx-exclude=_uuid.pyd")
    command_args.append("--upx-exclude=python3.dll")
    command_args.append("--upx-exclude=api-ms-win-core-file-l2-1-0.dll")
    command_args.append("--upx-exclude=*qt*")


command_args.append(f"main.py")

subprocess.call(command_args, cwd=project_path)  # noqa: s603

end = time.time()
print(f"\nBuild finished, took {round(end - start)}s.\n")

# update SW on network if built from master/main branch
if real_build:

    def compress_to_zip(input_dir, output_zip):
        with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
            for root, dirs, files in os.walk(input_dir):
                for file in files:
                    full_path = os.path.join(root, file)
                    zf.write(full_path, os.path.relpath(full_path, input_dir))

    local_zip_path = project_path / "dist" / f"{sw_name}_new.zip"
    compress_to_zip(project_path / "dist" / sw_name, local_zip_path)

    print("PRODUCTION BUILD: updating " + sw_name + " on the network...")
    start = time.time()

    # Safer copy of big file? :
    buffer_size = 1024 * 1024  # 1MB buffer size
    with open(local_zip_path, "rb") as src, open(network_sw_root / local_zip_path.name, "wb") as dst:
        shutil.copyfileobj(src, dst, buffer_size)

    network_sw_zip.unlink(missing_ok=True)

    new_network_zip = network_sw_root / local_zip_path.name
    new_network_zip.rename(network_sw_zip)

    end = time.time()
    print(f"\nSUCCESS: build was placed on the network, took {round(end - start)}s.\n")
    # print(f"{network_sw_zip}")
    print("Cleaning up...", end=" ")
    time.sleep(3)
    local_zip_path.unlink()
    print("Done!", end=" ")


# clean up created .spec file and build folder; not used & doesn't create slower build next time.
try:
    os.remove(f"{sw_name}.spec")  # noqa: PTH107 no FileNotFoundError; file will always be created
    shutil.rmtree("build")  # remove local "build" folder
except:
    print("(note: cleanup failed)")
