"""
Install face textures from 37 skin archives into AixBodySelector.
Auto-detects the correct internal path for each texture via 7z listing.
Falls back to CBBE for any missing texture.
"""
import subprocess, os, shutil, tempfile, re

SEVENZIP = r"C:\Program Files\7-Zip\7z.exe"
SKINDIR = r"G:\SteamLibrary\steamapps\common\MO2 2.5.2 for SkyrimVR\downloads\skin"
DLDIR   = r"G:\SteamLibrary\steamapps\common\MO2 2.5.2 for SkyrimVR\downloads"
MODROOT = r"G:\SteamLibrary\steamapps\common\MO2 2.5.2 for SkyrimVR\mods\RaceMenu Selector of Skins - Unique Player Character (Baby Girl)"

cbbe_files = [f for f in os.listdir(DLDIR) if f.startswith("Caliente")]
CBBE_ARCHIVE = os.path.join(DLDIR, cbbe_files[0])

# CBBE correct paths (found via debug)
CBBE_TEXTURES = {
    "femalehead.dds":     r"10 Face Pack\textures\actors\character\female\femalehead.dds",
    "femalehead_msn.dds": r"10 Face Pack\textures\actors\character\female\femalehead_msn.dds",
    "femalehead_s.dds":   r"10 Face Pack\textures\actors\character\female\femalehead_s.dds",
    "femalehead_sk.dds":  r"10 Face Pack\textures\actors\character\female\femalehead_sk.dds",
}

# Archive order (sorted = same order as survey)
ARCHIVE_ORDER = [
    "01 - Women of Skyrim - CBBE - Fomod Installer-20555-5--2-1594384891.7z",
    "03 - Leyenda Skin 4.0 CBBE 2K-10306-4-0.7z",
    "Aesthetic Skin CBBE SE-59086-1-0-1638155693.zip",
    "BI CBBE-24394-v2-3.7z",
    "Baby Girl CBBE-92195-2-1686399777.zip",
    "Barbarous Beauty CBBE 2048-38604-V1-1595569088.7z",
    "Bijin Skin CBBE-20078-1-4-1541714925.7z",
    "BnP female skin 2k (CBBE Player and Replacer)-65274-2-0-1688931865.7z",
    "DDG Skin 4K-65588-2-02-1650534890.7z",
    "DIBELLAN - True Skin for CBBE based bodies-63151-4-0-1646258246.7z",
    "Demoniac v1.12a - CBBE only - SE-19355-1-12a.7z",
    "Diamond 3BA puffy pussy normal maps-45718-2-6-1745768312.7z",
    "Diamond Textures CBBE v2 based on FSC v11-45718-2-6-1745767979.7z",
    "Eos Skin AIO-80326-1-21-1672829714.7z",
    "Fair Skin Complexion for CBBE v13.0-798-13-0-1770011213.7z",
    "GoldenVeil Skin-175578-1-00-1774462341.zip",
    "Lovergirl CBBE-83763-1-1675006751.zip",
    "Marshmallow Skin CBBE 4K-58713-1-1-1637547978.7z",
    "Mature Skin - CBBE-26017-2-15-2-1560516171.7z",
    "Mature Skin Complexion for CBBE-90848-1-2-1684056989.zip",
    "Noble Elegance Skin Textures - Author's Choice-106378-v1-00-1701974945.rar",
    "Northbourne Maiden Skin CBBE-61803-1-0-1641974520.7z",
    "PB's Silky Skin-95818-2-1-1721031275.zip",
    "Pride of Valhalla CBBE - Midgard-682-v1-3.rar",
    "Pure Suka Skin  v2.7z",
    "REALORE ULTIMA V2.1 - CBBE 4K-65577-2-1-1-1652866866.zip",
    "Real Girls Realistic Body Texture 2K (Original Version)-75065-6-0-1662842664.zip",
    "Reverie-64314-1-11-2-1727366169.7z",
    "Rogue Women of Skyrim CBBE-78938-1-0-1670496981.7z",
    "SG Female Textures Renewal-12938-1-4-1541252032.7z",
    "Sunkiss Skin 4K-70597-1-20-1658918615.7z",
    "Tempered Skins for Females CBBE-8505-1-32-1604152171.7z",
    "The Pure - CBBE-20583-1-3-1-1551788502.7z",
    "True North Maiden face and Body X.69.1 Beta 2k mix-51796-X-69-1-1636046428.7z",
    "Vera Skin v2-55334-2-6-1636796885.7z",
    "Zhizhenfemaleskin4K3BA-126288-3-6-1741347922.zip",
    "laogu 16Kskin CBBE 3BA-174370-1-5-97-1773138956.zip",
]

# Keywords to prefer/avoid when picking the best path
PREFER = ["default", "00", "base", "skin_d_base", "skin_n_base", "young", "medium"]
AVOID = ["freckle", "blemish", "mole", "scar", "dirt", "wet", "shiny", "gloss", "black",
         "vampire", "orc", "breton", "darkelf", "highelf", "imperial", "redguard", "woodelf",
         "femaleold", "succubus", "angelic", "vasc", "corrected", "tintmask"]

def score_path(path):
    """Lower is better."""
    p = path.lower()
    score = len(path)  # prefer shorter paths
    for kw in PREFER:
        if kw in p:
            score -= 50
    for kw in AVOID:
        if kw in p:
            score += 200
    # Strongly prefer paths in \female\ subfolder
    if r"\female\femalehead" in p.replace("/", "\\"):
        score -= 100
    return score

def list_archive_paths(archive_path, name_filter):
    """List all matching file paths in an archive (7z handles nested)."""
    r = subprocess.run(
        [SEVENZIP, "l", archive_path],
        capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    paths = []
    for line in r.stdout.splitlines():
        parts = line.strip().split()
        if not parts:
            continue
        candidate = parts[-1]
        if name_filter.lower() in candidate.lower():
            paths.append(candidate)
    return paths

def extract_one(archive_path, internal_path, dest_file):
    """Extract a single file from an archive (flat extract)."""
    tmp = tempfile.mkdtemp(prefix="aix_")
    try:
        subprocess.run(
            [SEVENZIP, "e", archive_path, internal_path, "-o" + tmp, "-y"],
            capture_output=True, text=True, encoding="utf-8", errors="replace"
        )
        extracted_name = os.path.basename(internal_path)
        src = os.path.join(tmp, extracted_name)
        if os.path.exists(src) and os.path.getsize(src) > 0:
            os.makedirs(os.path.dirname(dest_file), exist_ok=True)
            shutil.copy2(src, dest_file)
            return True
        # Also check case-insensitive
        for fn in os.listdir(tmp):
            if fn.lower() == extracted_name.lower() and os.path.getsize(os.path.join(tmp, fn)) > 0:
                os.makedirs(os.path.dirname(dest_file), exist_ok=True)
                shutil.copy2(os.path.join(tmp, fn), dest_file)
                return True
        return False
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

def find_best_path(archive_path, tex_name):
    """Auto-detect best matching path for tex_name in archive."""
    candidates = list_archive_paths(archive_path, tex_name)
    if not candidates:
        return None
    # Filter to exact filename match (case-insensitive)
    exact = [c for c in candidates if os.path.basename(c).lower() == tex_name.lower()]
    if not exact:
        return None
    # Sort by score
    exact.sort(key=score_path)
    return exact[0]

def install_texture(archive_path, tex_name, dest_file, label):
    """Find best path in archive and extract; return True on success."""
    best = find_best_path(archive_path, tex_name)
    if best is None:
        return False
    ok = extract_one(archive_path, best, dest_file)
    if ok:
        short = best if len(best) < 60 else "..." + best[-57:]
        print(f"    OK  {label} <- {short}")
    return ok

def install_cbbe(tex_name, dest_file):
    """Extract from CBBE fallback."""
    cbbe_path = CBBE_TEXTURES[tex_name]
    ok = extract_one(CBBE_ARCHIVE, cbbe_path, dest_file)
    if ok:
        print(f"    CBBE {tex_name}")
    else:
        print(f"    FAIL {tex_name} (CBBE also failed!)")
    return ok

def dest_dir(slot):
    return os.path.join(MODROOT, "textures", "aixbodyselector", f"skin{slot:02d}", "female")

TEX_NAMES = ["femalehead.dds", "femalehead_msn.dds", "femalehead_s.dds", "femalehead_sk.dds"]

# Pre-extract CBBE textures to a cache to avoid repeated extraction
print("Pre-caching CBBE textures...")
cbbe_cache = {}
cbbe_tmp = tempfile.mkdtemp(prefix="cbbe_cache_")
for tex in TEX_NAMES:
    dest = os.path.join(cbbe_tmp, tex)
    ok = extract_one(CBBE_ARCHIVE, CBBE_TEXTURES[tex], dest)
    if ok:
        cbbe_cache[tex] = dest
        print(f"  Cached {tex} ({os.path.getsize(dest):,} bytes)")
    else:
        print(f"  FAILED to cache {tex} from CBBE!")
print()

def install_cbbe_from_cache(tex_name, dest_file):
    if tex_name in cbbe_cache:
        os.makedirs(os.path.dirname(dest_file), exist_ok=True)
        shutil.copy2(cbbe_cache[tex_name], dest_file)
        print(f"    CBBE {tex_name}")
        return True
    print(f"    FAIL {tex_name} (CBBE cache missing!)")
    return False

# Slots 2-38: one archive each
for slot, archive_name in enumerate(ARCHIVE_ORDER, start=2):
    archive_path = os.path.join(SKINDIR, archive_name)
    print(f"\nSlot {slot:2d}: {archive_name}")
    destd = dest_dir(slot)
    for tex in TEX_NAMES:
        dest_file = os.path.join(destd, tex)
        ok = install_texture(archive_path, tex, dest_file, tex)
        if not ok:
            install_cbbe_from_cache(tex, dest_file)

# Slots 39-99: CBBE only
print(f"\nSlots 39-99: CBBE")
for slot in range(39, 100):
    destd = dest_dir(slot)
    print(f"  Slot {slot:2d}", end=" ", flush=True)
    for tex in TEX_NAMES:
        dest_file = os.path.join(destd, tex)
        if tex in cbbe_cache:
            os.makedirs(os.path.dirname(dest_file), exist_ok=True)
            shutil.copy2(cbbe_cache[tex], dest_file)
            print(".", end="", flush=True)
        else:
            print("X", end="", flush=True)
    print()

shutil.rmtree(cbbe_tmp, ignore_errors=True)
print("\nDone.")
