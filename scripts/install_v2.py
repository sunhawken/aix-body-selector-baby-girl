"""
install_v2.py — Authoritative texture installer for AixBodySelector.

Installs all 13 textures per slot (face + body + hands + blank) for slots 2-99.
Uses per-slot scoring keywords derived from the definitive source list.
Overwrites an existing file only when the incoming source is LARGER in size
(i.e., the installed file is smaller — we always keep the bigger/better version).
"""

import subprocess, os, shutil, tempfile, sys

SEVENZIP = r"C:\Program Files\7-Zip\7z.exe"
SKINDIR  = r"G:\SteamLibrary\steamapps\common\MO2 2.5.2 for SkyrimVR\downloads\skin"
DLDIR    = r"G:\SteamLibrary\steamapps\common\MO2 2.5.2 for SkyrimVR\downloads"
MODROOT  = (r"G:\SteamLibrary\steamapps\common\MO2 2.5.2 for SkyrimVR\mods"
            r"\RaceMenu Selector of Skins - Unique Player Character (Baby Girl)")

cbbe_files = [f for f in os.listdir(DLDIR) if f.startswith("Caliente")]
CBBE_ARCHIVE = os.path.join(DLDIR, cbbe_files[0])

# Slots 2-38 archive filenames in order
ARCHIVE_ORDER = [
    "01 - Women of Skyrim - CBBE - Fomod Installer-20555-5--2-1594384891.7z",       # slot 2
    "03 - Leyenda Skin 4.0 CBBE 2K-10306-4-0.7z",                                   # slot 3
    "Aesthetic Skin CBBE SE-59086-1-0-1638155693.zip",                               # slot 4
    "BI CBBE-24394-v2-3.7z",                                                         # slot 5
    "Baby Girl CBBE-92195-2-1686399777.zip",                                         # slot 6
    "Barbarous Beauty CBBE 2048-38604-V1-1595569088.7z",                             # slot 7
    "Bijin Skin CBBE-20078-1-4-1541714925.7z",                                       # slot 8
    "BnP female skin 2k (CBBE Player and Replacer)-65274-2-0-1688931865.7z",         # slot 9
    "DDG Skin 4K-65588-2-02-1650534890.7z",                                          # slot 10
    "DIBELLAN - True Skin for CBBE based bodies-63151-4-0-1646258246.7z",            # slot 11
    "Demoniac v1.12a - CBBE only - SE-19355-1-12a.7z",                               # slot 12
    "Diamond 3BA puffy pussy normal maps-45718-2-6-1745768312.7z",                   # slot 13
    "Diamond Textures CBBE v2 based on FSC v11-45718-2-6-1745767979.7z",             # slot 14
    "Eos Skin AIO-80326-1-21-1672829714.7z",                                         # slot 15
    "Fair Skin Complexion for CBBE v13.0-798-13-0-1770011213.7z",                    # slot 16
    "GoldenVeil Skin-175578-1-00-1774462341.zip",                                    # slot 17
    "Lovergirl CBBE-83763-1-1675006751.zip",                                         # slot 18
    "Marshmallow Skin CBBE 4K-58713-1-1-1637547978.7z",                              # slot 19
    "Mature Skin - CBBE-26017-2-15-2-1560516171.7z",                                 # slot 20
    "Mature Skin Complexion for CBBE-90848-1-2-1684056989.zip",                      # slot 21
    "Noble Elegance Skin Textures - Author's Choice-106378-v1-00-1701974945.rar",    # slot 22
    "Northbourne Maiden Skin CBBE-61803-1-0-1641974520.7z",                          # slot 23
    "PB's Silky Skin-95818-2-1-1721031275.zip",                                      # slot 24
    "Pride of Valhalla CBBE - Midgard-682-v1-3.rar",                                 # slot 25
    "Pure Suka Skin  v2.7z",                                                         # slot 26
    "REALORE ULTIMA V2.1 - CBBE 4K-65577-2-1-1-1652866866.zip",                      # slot 27
    "Real Girls Realistic Body Texture 2K (Original Version)-75065-6-0-1662842664.zip", # slot 28
    "Reverie-64314-1-11-2-1727366169.7z",                                            # slot 29
    "Rogue Women of Skyrim CBBE-78938-1-0-1670496981.7z",                            # slot 30
    "SG Female Textures Renewal-12938-1-4-1541252032.7z",                            # slot 31
    "Sunkiss Skin 4K-70597-1-20-1658918615.7z",                                      # slot 32
    "Tempered Skins for Females CBBE-8505-1-32-1604152171.7z",                       # slot 33
    "The Pure - CBBE-20583-1-3-1-1551788502.7z",                                     # slot 34
    "True North Maiden face and Body X.69.1 Beta 2k mix-51796-X-69-1-1636046428.7z",# slot 35
    "Vera Skin v2-55334-2-6-1636796885.7z",                                          # slot 36
    "Zhizhenfemaleskin4K3BA-126288-3-6-1741347922.zip",                              # slot 37
    "laogu 16Kskin CBBE 3BA-174370-1-5-97-1773138956.zip",                           # slot 38
]

ALL_TEX = [
    "femalehead.dds",     "femalehead_msn.dds",  "femalehead_s.dds",  "femalehead_sk.dds",
    "femalebody_1.dds",   "femalebody_1_msn.dds", "femalebody_1_s.dds","femalebody_1_sk.dds",
    "femalehands_1.dds",  "femalehands_1_msn.dds","femalehands_1_s.dds","femalehands_1_sk.dds",
    "blankdetailmap.dds",
]

# CBBE archive internal paths for every texture
CBBE_PATHS = {
    "femalehead.dds":      r"10 Face Pack\textures\actors\character\female\femalehead.dds",
    "femalehead_msn.dds":  r"10 Face Pack\textures\actors\character\female\femalehead_msn.dds",
    "femalehead_s.dds":    r"10 Face Pack\textures\actors\character\female\femalehead_s.dds",
    "femalehead_sk.dds":   r"10 Face Pack\textures\actors\character\female\femalehead_sk.dds",
    "femalebody_1.dds":    r"00 Required (Slim)\textures\actors\character\female\femalebody_1.dds",
    "femalebody_1_msn.dds":r"00 Required (Slim)\textures\actors\character\female\femalebody_1_msn.dds",
    "femalebody_1_s.dds":  r"00 Required (Slim)\textures\actors\character\female\femalebody_1_s.dds",
    "femalebody_1_sk.dds": r"00 Required (Slim)\textures\actors\character\female\femalebody_1_sk.dds",
    "femalehands_1.dds":   r"00 Required (Slim)\textures\actors\character\female\femalehands_1.dds",
    "femalehands_1_msn.dds":r"00 Required (Slim)\textures\actors\character\female\femalehands_1_msn.dds",
    "femalehands_1_s.dds": r"00 Required (Slim)\textures\actors\character\female\femalehands_1_s.dds",
    "femalehands_1_sk.dds":r"00 Required (Slim)\textures\actors\character\female\femalehands_1_sk.dds",
    "blankdetailmap.dds":  r"10 Face Pack\textures\actors\character\male\blankdetailmap.dds",
}

# ─── Global scoring ───────────────────────────────────────────────────────────
PREFER_GLOBAL = ["default", "00 default", "00main", "base", "slim", "young", "medium", "skin_d"]
AVOID_GLOBAL  = [
    "freckle", "blemish", "mole", "scar", "dirt", "wet", "shiny", "gloss", "black",
    "vampire", "orc", "breton", "darkelf", "highelf", "imperial", "redguard", "woodelf",
    "femaleold", "succubus", "angelic", "vasc", "male\\femalebody", "male/femalebody",
    "fomod", ".xml", ".txt", ".png", ".jpg", "mesh", "tintmask", "corrected",
]

# ─── Per-slot extra prefer keywords ──────────────────────────────────────────
# These are applied in addition to PREFER_GLOBAL (each hit = -50 score)
SLOT_PREFER = {
    2:  ["shaved", "slim"],
    3:  ["slim", "bniples", "leaf", "silky", "medium", "muscles"],
    4:  ["pubic", "shaved", "figure"],
    7:  ["sunburn", "muscular", "10%", "common"],
    8:  ["pubic", "2k"],
    9:  ["veiny", "big", "soft"],
    10: ["00base", "muscle_n", "mature_s", "sss"],
    11: ["bare", "2k"],
    12: ["rg_2k", "n_base", "s_g_4k", "rg", "g_4k"],
    13: ["puffy", "chubby"],
    14: ["v8", "lips", "nred", "shaved", "chubby", "v2.6"],
    16: ["slim", "silky"],
    20: ["young", "moles", "complexion"],
    21: ["my version"],
    24: ["paw", "smooth"],
    27: ["niptype", "shaved", "smooth", "common", "ultima"],
    29: ["aging", "ece", "unshaved", "strong", "required"],
    30: ["1hairy", "hairy", "0normal", "0default", "0common"],
    31: ["slim", "dark"],
    33: ["clean", "hairy", "fit", "lesser", "0-common"],
    34: ["pubic", "4k", "slim", "wet", "0-base"],
    35: ["x_69", "beta", "2k"],
}

# ─── Per-slot textures that MUST use CBBE (never try the archive) ────────────
SLOT_FORCE_CBBE = {
    5:  ["femalehead_sk.dds", "femalebody_1_sk.dds", "femalehands_1_sk.dds",
         "blankdetailmap.dds"],
    7:  ["blankdetailmap.dds"],
    10: ["blankdetailmap.dds"],
    12: ["blankdetailmap.dds"],
    13: [  # normals-only archive — only _msn comes from archive
        "femalehead.dds",    "femalehead_s.dds",    "femalehead_sk.dds",
        "femalebody_1.dds",  "femalebody_1_s.dds",  "femalebody_1_sk.dds",
        "femalehands_1.dds", "femalehands_1_s.dds", "femalehands_1_sk.dds",
        "blankdetailmap.dds",
    ],
    15: [  # no diffuse DDS in archive
        "femalehead.dds", "femalebody_1.dds", "femalehands_1.dds", "blankdetailmap.dds",
    ],
    17: [  # diffuse-only archive
        "femalehead_msn.dds",  "femalehead_s.dds",    "femalehead_sk.dds",
        "femalebody_1_msn.dds","femalebody_1_s.dds",  "femalebody_1_sk.dds",
        "femalehands_1_msn.dds","femalehands_1_s.dds","femalehands_1_sk.dds",
        "blankdetailmap.dds",
    ],
    19: [  # diffuse-only archive
        "femalehead_msn.dds",  "femalehead_s.dds",    "femalehead_sk.dds",
        "femalebody_1_msn.dds","femalebody_1_s.dds",  "femalebody_1_sk.dds",
        "femalehands_1_msn.dds","femalehands_1_s.dds","femalehands_1_sk.dds",
        "blankdetailmap.dds",
    ],
    25: ["blankdetailmap.dds"],
    26: ["blankdetailmap.dds"],
    28: [  # diffuse-only archive
        "femalehead_msn.dds",  "femalehead_s.dds",    "femalehead_sk.dds",
        "femalebody_1_msn.dds","femalebody_1_s.dds",  "femalebody_1_sk.dds",
        "femalehands_1_msn.dds","femalehands_1_s.dds","femalehands_1_sk.dds",
        "blankdetailmap.dds",
    ],
    32: ["blankdetailmap.dds"],
    36: ["blankdetailmap.dds"],
    37: ["femalebody_1.dds", "femalebody_1_msn.dds"],   # Chinese-char encoding issue in 7z
    38: ["blankdetailmap.dds"],
}

# ─── Helpers ─────────────────────────────────────────────────────────────────

def make_scorer(slot):
    """Return a scoring function tuned for this slot."""
    extra_prefer = SLOT_PREFER.get(slot, [])
    def score(path):
        p = path.lower().replace("/", "\\")
        s = len(path)
        for kw in PREFER_GLOBAL:
            if kw in p: s -= 50
        for kw in extra_prefer:
            if kw in p: s -= 60          # slightly stronger than global
        for kw in AVOID_GLOBAL:
            if kw in p: s += 200
        # Strongly prefer paths that sit directly in a \female\ subfolder
        if r"\female\femalebody"  in p: s -= 100
        if r"\female\femalehands" in p: s -= 100
        if r"\female\femalehead"  in p: s -= 100
        return s
    return score

def list_slt(archive_path, name_filter):
    """Return all internal paths whose basename == name_filter (case-insensitive), via -slt."""
    r = subprocess.run(
        [SEVENZIP, "l", "-slt", archive_path],
        capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    paths = []
    for line in r.stdout.splitlines():
        if line.startswith("Path = "):
            candidate = line[7:].strip()
            if os.path.basename(candidate).lower() == name_filter.lower():
                paths.append(candidate)
    return paths

def extract_to_temp(archive_path, internal_path):
    """Extract a single file to a temp dir. Returns (tmp_dir, filepath) or (tmp_dir, None)."""
    tmp = tempfile.mkdtemp(prefix="aix2_")
    subprocess.run(
        [SEVENZIP, "e", archive_path, internal_path, "-o" + tmp, "-y"],
        capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    fname = os.path.basename(internal_path)
    for fn in os.listdir(tmp):
        if fn.lower() == fname.lower():
            src = os.path.join(tmp, fn)
            if os.path.getsize(src) > 0:
                return tmp, src
    return tmp, None

def install_file(src_path, dest_file):
    """
    Copy src_path to dest_file.
    Overwrites existing only if src is LARGER than existing (overwrite-if-smaller logic).
    Returns: 'installed', 'overwritten', 'skipped', or 'error'
    """
    src_size = os.path.getsize(src_path)
    if src_size == 0:
        return "error"
    os.makedirs(os.path.dirname(dest_file), exist_ok=True)
    if os.path.exists(dest_file):
        existing_size = os.path.getsize(dest_file)
        if existing_size >= src_size:
            return "skipped"           # existing is same or larger — keep it
        shutil.copy2(src_path, dest_file)
        return "overwritten"
    shutil.copy2(src_path, dest_file)
    return "installed"

def find_and_install(archive_path, tex_name, dest_file, scorer):
    """Find best path in archive for tex_name, extract, and install. Returns status string."""
    candidates = list_slt(archive_path, tex_name)
    if not candidates:
        return None     # not in archive
    candidates.sort(key=scorer)
    for path in candidates[:3]:
        tmp, src = extract_to_temp(archive_path, path)
        try:
            if src:
                status = install_file(src, dest_file)
                short = path if len(path) < 60 else "…" + path[-57:]
                return f"{status}:{short}"
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    return None     # all candidates failed extraction

# ─── Pre-cache CBBE textures ─────────────────────────────────────────────────
print("Pre-caching CBBE textures...", flush=True)
cbbe_tmp  = tempfile.mkdtemp(prefix="cbbe2_")
cbbe_cache = {}
for tex, cbbe_path in CBBE_PATHS.items():
    dest = os.path.join(cbbe_tmp, tex)
    tmp, src = extract_to_temp(CBBE_ARCHIVE, cbbe_path)
    if src:
        shutil.copy2(src, dest)
        cbbe_cache[tex] = dest
        print(f"  OK  {tex:35s} ({os.path.getsize(dest):>9,})", flush=True)
    else:
        print(f"  FAIL {tex}", flush=True)
    shutil.rmtree(tmp, ignore_errors=True)
print()

def install_cbbe(tex_name, dest_file):
    if tex_name not in cbbe_cache:
        return "cbbe_missing"
    tmp_src = cbbe_cache[tex_name]
    status = install_file(tmp_src, dest_file)
    return f"cbbe:{status}"

def dest_dir(slot):
    return os.path.join(MODROOT, "textures", "aixbodyselector", f"skin{slot:02d}", "female")

# ─── Install slots 2-38 ───────────────────────────────────────────────────────
for slot, archive_name in enumerate(ARCHIVE_ORDER, start=2):
    archive_path = os.path.join(SKINDIR, archive_name)
    force_cbbe   = set(SLOT_FORCE_CBBE.get(slot, []))
    scorer       = make_scorer(slot)
    destd        = dest_dir(slot)
    print(f"\nSlot {slot:02d}: {archive_name[:55]}…", flush=True)

    for tex in ALL_TEX:
        dest_file = os.path.join(destd, tex)

        if tex in force_cbbe:
            status = install_cbbe(tex, dest_file)
            print(f"  [CBBE/{status.split(':')[-1]:>11}] {tex}", flush=True)
            continue

        result = find_and_install(archive_path, tex, dest_file, scorer)
        if result:
            tag, path = result.split(":", 1)
            print(f"  [{tag:>12}] {tex:30s} ← {path}", flush=True)
        else:
            # Fallback to CBBE
            status = install_cbbe(tex, dest_file)
            print(f"  [CBBE/{status.split(':')[-1]:>11}] {tex}  (not in archive)", flush=True)

# ─── Install slots 39-99 (all CBBE) ──────────────────────────────────────────
print("\nSlots 39-99: CBBE only", flush=True)
ok_count = 0
for slot in range(39, 100):
    destd = dest_dir(slot)
    for tex in ALL_TEX:
        dest_file = os.path.join(destd, tex)
        status = install_cbbe(tex, dest_file)
        if "installed" in status or "overwritten" in status:
            ok_count += 1
    print(f"  Slot {slot:02d} done", flush=True)

# ─── Cleanup ─────────────────────────────────────────────────────────────────
shutil.rmtree(cbbe_tmp, ignore_errors=True)
print(f"\nAll done. Slots 39-99: {ok_count} files written.")
