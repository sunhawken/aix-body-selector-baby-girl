"""Install body/hands/blankdetailmap textures for all slots 2-99."""
import subprocess, os, shutil, tempfile

SEVENZIP = r"C:\Program Files\7-Zip\7z.exe"
SKINDIR  = r"G:\SteamLibrary\steamapps\common\MO2 2.5.2 for SkyrimVR\downloads\skin"
DLDIR    = r"G:\SteamLibrary\steamapps\common\MO2 2.5.2 for SkyrimVR\downloads"
MODROOT  = r"G:\SteamLibrary\steamapps\common\MO2 2.5.2 for SkyrimVR\mods\RaceMenu Selector of Skins - Unique Player Character (Baby Girl)"

cbbe_files = [f for f in os.listdir(DLDIR) if f.startswith("Caliente")]
CBBE_ARCHIVE = os.path.join(DLDIR, cbbe_files[0])

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

# CBBE fallback paths
CBBE_BODY = {
    "femalebody_1.dds":     r"00 Required (Slim)\textures\actors\character\female\femalebody_1.dds",
    "femalebody_1_msn.dds": r"00 Required (Slim)\textures\actors\character\female\femalebody_1_msn.dds",
    "femalebody_1_s.dds":   r"00 Required (Slim)\textures\actors\character\female\femalebody_1_s.dds",
    "femalebody_1_sk.dds":  r"00 Required (Slim)\textures\actors\character\female\femalebody_1_sk.dds",
    "femalehands_1.dds":     r"00 Required (Slim)\textures\actors\character\female\femalehands_1.dds",
    "femalehands_1_msn.dds": r"00 Required (Slim)\textures\actors\character\female\femalehands_1_msn.dds",
    "femalehands_1_s.dds":   r"00 Required (Slim)\textures\actors\character\female\femalehands_1_s.dds",
    "femalehands_1_sk.dds":  r"00 Required (Slim)\textures\actors\character\female\femalehands_1_sk.dds",
    "blankdetailmap.dds":    r"10 Face Pack\textures\actors\character\male\blankdetailmap.dds",
}

BODY_TEX = [
    "femalebody_1.dds", "femalebody_1_msn.dds", "femalebody_1_s.dds", "femalebody_1_sk.dds",
    "femalehands_1.dds", "femalehands_1_msn.dds", "femalehands_1_s.dds", "femalehands_1_sk.dds",
    "blankdetailmap.dds",
]

PREFER = ["default", "00 default", "00main", "base", "slim", "skin_d", "young", "medium"]
AVOID  = ["freckle", "blemish", "mole", "scar", "dirt", "wet", "shiny", "gloss", "black",
          "vampire", "orc", "breton", "darkelf", "highelf", "imperial", "redguard", "woodelf",
          "femaleold", "succubus", "angelic", "vasc", "male\\femalebody", "male/femalebody",
          "fomod", ".xml", ".txt", ".png", ".jpg", "mesh"]

def score_path(path):
    p = path.lower()
    score = len(path)
    for kw in PREFER:
        if kw in p:
            score -= 50
    for kw in AVOID:
        if kw in p:
            score += 200
    if r"\female\femalebody" in p or "/female/femalebody" in p:
        score -= 100
    if r"\female\femalehands" in p or "/female/femalehands" in p:
        score -= 100
    return score

def list_slt(archive_path, name_filter):
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
    for path in candidates[:3]:
        if extract_one(archive_path, path, dest_file):
            return True, path
    return False, candidates[0] if candidates else None

# Pre-cache CBBE textures
print("Pre-caching CBBE body textures...")
cbbe_tmp = tempfile.mkdtemp(prefix="cbbe_body_")
cbbe_cache = {}
for tex, cbbe_path in CBBE_BODY.items():
    dest = os.path.join(cbbe_tmp, tex)
    if extract_one(CBBE_ARCHIVE, cbbe_path, dest):
        cbbe_cache[tex] = dest
        print(f"  Cached {tex} ({os.path.getsize(dest):,} bytes)")
    else:
        print(f"  FAILED to cache {tex} from CBBE!")
print()

def install_from_cbbe(tex_name, dest_file):
    if tex_name in cbbe_cache:
        os.makedirs(os.path.dirname(dest_file), exist_ok=True)
        shutil.copy2(cbbe_cache[tex_name], dest_file)
        return True
    return False

def dest_dir(slot):
    return os.path.join(MODROOT, "textures", "aixbodyselector", f"skin{slot:02d}", "female")

# Install slots 2-38 from skin archives
for slot, archive_name in enumerate(ARCHIVE_ORDER, start=2):
    archive_path = os.path.join(SKINDIR, archive_name)
    print(f"\nSlot {slot:2d}: {archive_name}")
    destd = dest_dir(slot)
    for tex in BODY_TEX:
        dest_file = os.path.join(destd, tex)
        if os.path.exists(dest_file) and os.path.getsize(dest_file) > 0:
            print(f"    SKIP {tex} (exists)")
            continue
        ok, path = find_and_extract(archive_path, tex, dest_file)
        if ok:
            short = path if len(path) < 65 else "..." + path[-62:]
            print(f"    OK   {tex} <- {short}")
        else:
            ok2 = install_from_cbbe(tex, dest_file)
            print(f"    {'CBBE' if ok2 else 'FAIL'} {tex}")

# Slots 39-99: CBBE only
print("\nSlots 39-99: CBBE")
for slot in range(39, 100):
    destd = dest_dir(slot)
    print(f"  Slot {slot:2d}", end=" ", flush=True)
    for tex in BODY_TEX:
        dest_file = os.path.join(destd, tex)
        if os.path.exists(dest_file) and os.path.getsize(dest_file) > 0:
            print(".", end="", flush=True)
            continue
        ok = install_from_cbbe(tex, dest_file)
        print("." if ok else "X", end="", flush=True)
    print()

shutil.rmtree(cbbe_tmp, ignore_errors=True)
print("\nDone.")
