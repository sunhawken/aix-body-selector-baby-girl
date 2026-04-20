"""Re-extract slots that fell back to CBBE due to path-with-spaces bug."""
import subprocess, os, shutil, tempfile

SEVENZIP = r"C:\Program Files\7-Zip\7z.exe"
SKINDIR  = r"G:\SteamLibrary\steamapps\common\MO2 2.5.2 for SkyrimVR\downloads\skin"
DLDIR    = r"G:\SteamLibrary\steamapps\common\MO2 2.5.2 for SkyrimVR\downloads"
MODROOT  = r"G:\SteamLibrary\steamapps\common\MO2 2.5.2 for SkyrimVR\mods\RaceMenu Selector of Skins - Unique Player Character (Baby Girl)"

cbbe_files = [f for f in os.listdir(DLDIR) if f.startswith("Caliente")]
CBBE_ARCHIVE = os.path.join(DLDIR, cbbe_files[0])

PREFER = ["default", "00 default", "00main", "base", "skin_d", "skin_n", "skin_s", "skin_sk", "young", "medium", "life", "smoother"]
AVOID  = ["freckle", "blemish", "mole", "scar", "dirt", "wet", "shiny", "gloss", "black",
          "vampire", "orc", "breton", "darkelf", "highelf", "imperial", "redguard", "woodelf",
          "femaleold", "succubus", "angelic", "vasc", "corrected", "tintmask", "screen", "fomod",
          "hardened", "aging", "mesh", "mesh", ".xml", ".txt", ".png", ".jpg"]

def score_path(path):
    p = path.lower()
    score = len(path)
    for kw in PREFER:
        if kw in p:
            score -= 50
    for kw in AVOID:
        if kw in p:
            score += 200
    if r"\female\femalehead" in p or "/female/femalehead" in p:
        score -= 100
    return score

def list_slt(archive_path, name_filter):
    """List archive using -slt for unambiguous paths (handles spaces)."""
    r = subprocess.run([SEVENZIP, "l", "-slt", archive_path],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    paths = []
    for line in r.stdout.splitlines():
        if line.startswith("Path = "):
            candidate = line[7:]
            if os.path.basename(candidate).lower() == name_filter.lower():
                paths.append(candidate)
    return paths

def extract_one(archive_path, internal_path, dest_file):
    tmp = tempfile.mkdtemp(prefix="aix_")
    try:
        subprocess.run(
            [SEVENZIP, "e", archive_path, internal_path, "-o" + tmp, "-y"],
            capture_output=True, text=True, encoding="utf-8", errors="replace"
        )
        expected = os.path.basename(internal_path)
        for fn in os.listdir(tmp):
            if fn.lower() == expected.lower() and os.path.getsize(os.path.join(tmp, fn)) > 0:
                os.makedirs(os.path.dirname(dest_file), exist_ok=True)
                shutil.copy2(os.path.join(tmp, fn), dest_file)
                return True
        return False
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

def find_and_extract(archive_path, tex_name, dest_file):
    candidates = list_slt(archive_path, tex_name)
    if not candidates:
        return False, None
    candidates.sort(key=score_path)
    for path in candidates[:3]:  # try top 3 candidates
        ok = extract_one(archive_path, path, dest_file)
        if ok:
            return True, path
    return False, candidates[0] if candidates else None

TEX_NAMES = ["femalehead.dds", "femalehead_msn.dds", "femalehead_s.dds", "femalehead_sk.dds"]

# Archives that previously fell back to CBBE — re-try with fixed path detection
RETRY = {
    2:  "01 - Women of Skyrim - CBBE - Fomod Installer-20555-5--2-1594384891.7z",
    4:  "Aesthetic Skin CBBE SE-59086-1-0-1638155693.zip",
    5:  "BI CBBE-24394-v2-3.7z",
    7:  "Barbarous Beauty CBBE 2048-38604-V1-1595569088.7z",
    8:  "Bijin Skin CBBE-20078-1-4-1541714925.7z",
    9:  "BnP female skin 2k (CBBE Player and Replacer)-65274-2-0-1688931865.7z",
    11: "DIBELLAN - True Skin for CBBE based bodies-63151-4-0-1646258246.7z",
    13: "Diamond 3BA puffy pussy normal maps-45718-2-6-1745768312.7z",
    14: "Diamond Textures CBBE v2 based on FSC v11-45718-2-6-1745767979.7z",
    16: "Fair Skin Complexion for CBBE v13.0-798-13-0-1770011213.7z",
    21: "Mature Skin Complexion for CBBE-90848-1-2-1684056989.zip",
    24: "PB's Silky Skin-95818-2-1-1721031275.zip",
    25: "Pride of Valhalla CBBE - Midgard-682-v1-3.rar",
    29: "Reverie-64314-1-11-2-1727366169.7z",
    31: "SG Female Textures Renewal-12938-1-4-1541252032.7z",
    33: "Tempered Skins for Females CBBE-8505-1-32-1604152171.7z",
    34: "The Pure - CBBE-20583-1-3-1-1551788502.7z",
    35: "True North Maiden face and Body X.69.1 Beta 2k mix-51796-X-69-1-1636046428.7z",
    37: "Zhizhenfemaleskin4K3BA-126288-3-6-1741347922.zip",
}

for slot, archive_name in sorted(RETRY.items()):
    archive_path = os.path.join(SKINDIR, archive_name)
    destd = os.path.join(MODROOT, "textures", "aixbodyselector", f"skin{slot:02d}", "female")
    print(f"\nSlot {slot:2d}: {archive_name}")
    for tex in TEX_NAMES:
        dest_file = os.path.join(destd, tex)
        ok, path = find_and_extract(archive_path, tex, dest_file)
        if ok:
            short = path if len(path) < 70 else "..." + path[-67:]
            print(f"    OK  {tex} <- {short}")
        else:
            existing_size = os.path.getsize(dest_file) if os.path.exists(dest_file) else 0
            print(f"    KEEP {tex} (already CBBE, {existing_size:,} bytes)")

print("\nDone.")
