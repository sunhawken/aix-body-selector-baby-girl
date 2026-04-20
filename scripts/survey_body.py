"""Survey archives for body + hands textures and blankdetailmap."""
import subprocess, os

SEVENZIP = r"C:\Program Files\7-Zip\7z.exe"
SKINDIR  = r"G:\SteamLibrary\steamapps\common\MO2 2.5.2 for SkyrimVR\downloads\skin"
DLDIR    = r"G:\SteamLibrary\steamapps\common\MO2 2.5.2 for SkyrimVR\downloads"

cbbe_files = [f for f in os.listdir(DLDIR) if f.startswith("Caliente")]
CBBE = os.path.join(DLDIR, cbbe_files[0])

TARGETS = ["femalebody_1.dds", "femalehands_1.dds", "blankdetailmap.dds"]

def list_slt(archive_path):
    r = subprocess.run([SEVENZIP, "l", "-slt", archive_path],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    paths = []
    for line in r.stdout.splitlines():
        if line.startswith("Path = "):
            paths.append(line[7:])
    return paths

# Check CBBE first
print("=== CBBE ===")
cbbe_paths = list_slt(CBBE)
for t in TARGETS:
    matches = [p for p in cbbe_paths if os.path.basename(p).lower() == t.lower()]
    # Filter to standard female/ path
    std = [m for m in matches if r"\female\femalebody" in m.lower() or r"\female\femalehands" in m.lower() or "blank" in m.lower()]
    print(f"  {t}: {std[:2] if std else matches[:2]}")

archives = sorted(os.listdir(SKINDIR))
for arch in archives:
    path = os.path.join(SKINDIR, arch)
    paths = list_slt(path)
    print(f"\n=== {arch} ===")
    for t in TARGETS:
        matches = [p for p in paths if os.path.basename(p).lower() == t.lower()]
        std = [m for m in matches if "female" in m.lower() or "blank" in m.lower()]
        # Pick best: shortest path in female/ subfolder
        best = sorted(std, key=len)[:2] if std else sorted(matches, key=len)[:2]
        print(f"  {t}: {best}")
