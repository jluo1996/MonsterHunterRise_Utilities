import sys
import re
from pathlib import Path

if len(sys.argv) != 7:
    print("There were only {len(sys.argv)-1} arguments provided.")
    for i, arg in enumerate(sys.argv):
        print(f"  Arg {i}: {arg}")
    sys.exit(1)

app_name = sys.argv[1]
major = sys.argv[2]
minor = sys.argv[3]
build = "0" # sys.argv[4] # NOTE: the git build version number is larger than Windows rule 65535
revision = sys.argv[5]
version_file = Path(sys.argv[6])

version = f"{major}.{minor}.{build}.{revision}"
tuple_version = f"({major}, {minor}, {build}, {revision})"
print(f"Setting version to {version} in {version_file.resolve()}")

text = version_file.read_text(encoding="utf-8")

# ================ Update version info in the file ================
# --- Replace numeric versions ---
text = re.sub(
    r"filevers=\([^)]+\)",
    f"filevers={tuple_version}",
    text
)

text = re.sub(
    r"prodvers=\([^)]+\)",
    f"prodvers={tuple_version}",
    text
)

# --- Replace string versions ---
text = re.sub(
    r"StringStruct\('FileVersion',\s*'[^']*'\)",
    f"StringStruct('FileVersion', '{version}')",
    text
)

text = re.sub(
    r"StringStruct\('ProductVersion',\s*'[^']*'\)",
    f"StringStruct('ProductVersion', '{version}')",
    text
)

print(f"Updated version to {version}")
# ================================================================


# ================ Update all names in the file ================
# --- Replace product name using app_name ---
text = re.sub(
    r"StringStruct\('ProductName',\s*'[^']*'\)",
    f"StringStruct('ProductName', '{app_name}')",
    text
)
text = re.sub(
    r"StringStruct\('InternalName',\s*'[^']*'\)",
    f"StringStruct('InternalName', '{app_name}')",
    text
)
text = re.sub(
    r"StringStruct\('OriginalFilename',\s*'[^']*'\)",
    f"StringStruct('OriginalFilename', '{app_name}.exe')",
    text
)
print(f"Updated names to {app_name}")
# ================================================================

version_file.write_text(text, encoding="utf-8")
print(f"Updated file: {version_file.resolve()}")
