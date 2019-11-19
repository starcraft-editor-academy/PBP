import os
import string


for the_file in os.listdir("eds"):
    file_path = os.path.join("eds", the_file)
    if os.path.isfile(file_path):
        os.unlink(file_path)
with open("source/VERSION", "r") as f:
    VERSION = f.read()
edslist = []
for root, dirs, files in os.walk("basemap"):
    for file in files:
        if not (file.startswith("(") and file.endswith(".scx")) or file[-5] in "()":
            continue
        eds = file = file[:-4]
        forbidden_chars = string.digits + string.whitespace + string.punctuation
        for c in forbidden_chars:
            eds = eds.replace(c, "")
        print(file, eds)
        edslist.append(eds)
        with open(f"eds/{eds}.eds", "w") as e:
            outpath = "" if root == "basemap" else f"{root[8:]}\\"
            e.write(
                f"""[main]
input:  ..\{root}\{file}.scx
output: ..\output\{outpath}{file}_PBP{VERSION}.scx

[../source/main.py]
[freeze]
freeze: 0
"""
            )

with open(f"make.ps1", "w") as d:
    d.write(
        """Remove-Item PBP_TEST.scx
cd output
Get-ChildItem *.scx -Recurse | Where { ! $_.PSIsContainer } | Remove-Item
cd ..
.\source\TEST.eds
cd eds
"""
    )
    for eds in edslist:
        d.write(f"Start-Process .\{eds}.eds -windowstyle hidden\n")
    d.write("cd ..")
