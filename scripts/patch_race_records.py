"""
Patch all NakedHands and NakedFeet YAML files to include the 4 vampire races
that are in NakedTorso but missing from NakedHands/NakedFeet.

Missing races (confirmed by diff between Torso and Hands):
  08883D:Skyrim.esm
  088840:Skyrim.esm
  088884:Skyrim.esm
  097A3D:Skyrim.esm
"""
import os, re

AA_DIR = r"C:\tmp\aix-yaml2\ArmorAddons"

# Full correct 17-race list (same as NakedTorso)
FULL_RACES = """\
AdditionalRaces:
- 013741:Skyrim.esm
- 013742:Skyrim.esm
- 013743:Skyrim.esm
- 013744:Skyrim.esm
- 013746:Skyrim.esm
- 013747:Skyrim.esm
- 013748:Skyrim.esm
- 013749:Skyrim.esm
- 088794:Skyrim.esm
- 08883C:Skyrim.esm
- 08883D:Skyrim.esm
- 088840:Skyrim.esm
- 088844:Skyrim.esm
- 088846:Skyrim.esm
- 088884:Skyrim.esm
- 097A3D:Skyrim.esm
- 0A82B9:Skyrim.esm"""

updated = 0
skipped = 0
errors  = 0

for fn in sorted(os.listdir(AA_DIR)):
    if not (("NakedHands" in fn or "NakedFeet" in fn) and fn.endswith(".yaml")):
        continue
    path = os.path.join(AA_DIR, fn)
    with open(path, encoding="utf-8") as f:
        content = f.read()

    # Replace the AdditionalRaces block (from "AdditionalRaces:" to next blank line or EOF)
    new_content = re.sub(
        r"AdditionalRaces:\n(?:- [^\n]+\n)+",
        FULL_RACES + "\n",
        content
    )

    if new_content == content:
        # Check if it already has all 4 races
        if "08883D:Skyrim.esm" in content and "097A3D:Skyrim.esm" in content:
            skipped += 1
        else:
            print(f"WARN: No replacement made for {fn}")
            errors += 1
        continue

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    updated += 1

print(f"\nDone: {updated} files updated, {skipped} already correct, {errors} errors")
