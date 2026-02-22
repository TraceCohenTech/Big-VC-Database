#!/usr/bin/env python3
"""
Merge curated VCs with original list, removing only clearly invalid entries
"""

import re

# Read the curated data (with correct sector tags for major VCs)
with open('data.js', 'r') as f:
    curated_content = f.read()

# Read the original data (755 VCs)
with open('data_original.js', 'r') as f:
    original_content = f.read()

# Parse VCs from content
def parse_vcs(content):
    vcs = []
    pattern = r'\{name:"([^"]*)",location:"([^"]*)",region:"([^"]*)",stages:\[(.*?)\],sectors:\[(.*?)\],check_size:"([^"]*)",aum:"([^"]*)"\}'
    for m in re.finditer(pattern, content):
        name, location, region, stages_str, sectors_str, check_size, aum = m.groups()
        stages = [s.strip().strip('"') for s in stages_str.split(',') if s.strip().strip('"')]
        sectors = [s.strip().strip('"') for s in sectors_str.split(',') if s.strip().strip('"')]
        vcs.append({
            'name': name,
            'location': location,
            'region': region,
            'stages': stages,
            'sectors': sectors,
            'check_size': check_size,
            'aum': aum
        })
    return vcs

curated_vcs = parse_vcs(curated_content)
original_vcs = parse_vcs(original_content)

print(f"Curated VCs: {len(curated_vcs)}")
print(f"Original VCs: {len(original_vcs)}")

# Create set of curated VC names (lowercase for matching)
curated_names = {vc['name'].lower() for vc in curated_vcs}

# Patterns to REMOVE (invalid entries)
INVALID_PATTERNS = [
    r'^[A-Z][a-z]{0,4}$',  # Too short names like "Hum", "Neo", "Morg", etc.
    r'\($',                # Truncated parentheses
    r'^\d+$',              # Just numbers
]

# Specific names to REMOVE (defunct, invalid, duplicates)
REMOVE_NAMES = {
    '100 black angels',
    'a capital*',
    'countdown capital',
    'sap.io',
    'foo',
    'google',
    'cle', 'col', 'fin', 'edu', 'gan', 'comm', 'hum', 'neo', 'par',
    'khos', 'morg', 'nest', 'out', 'sca', 'pil', 'may', 'kim', 'left',
    'jump', 'inter', 'insight', 'matrix', 'hyper', 'hyperp', 'inerti',
    'mush', 'metap', 'robo', 'radi', 'rab', 'selv', 'seren', 'shast',
    'shim', 'sigm', 'sierr', 'sequoi', 'mendoz', 'meridi', 'newpath',
    'next p', 'patron', 'panter', 'quon', 'remote', 'rocan', 'red se',
    'red sw', 'nerud', 'looking g', 'kupand', 'mubada',
    # Duplicates of curated entries
    'bessemer venture', 'coatue', 'greylock', 'greylockvc',
    'gvfinancially', 'felicis venturesprioritizes', 'ggv capitalbuilt',
    'ivpseries b', 'lightspeed venture', 'new enterprise associates (nea',
}

# Names with attached descriptions to clean
NAME_HAS_DESCRIPTION = [
    'Hustle FundHi', 'IVPSeries B', 'Lightspeed Venture',
    'New Enterprise Associates (NEA', 'OrbiMed AdvisorsHealthcare-only',
    'MaveronConsumer-only', 'Menlo Ventures$500M Inflection Fund',
    'Innospark VenturesAI-only',
]

def is_valid_vc(vc):
    name = vc['name']
    name_lower = name.lower()

    # Check against remove list
    if name_lower in REMOVE_NAMES:
        return False, "In remove list"

    # Check for invalid patterns
    for pattern in INVALID_PATTERNS:
        if re.match(pattern, name):
            return False, f"Matches invalid pattern: {pattern}"

    # Check for attached descriptions (description text merged with name)
    # Only flag if it has CamelCase AND the name is unusually long (>25 chars)
    # suggesting description text was appended
    if len(name) > 25 and re.search(r'[a-z][A-Z][a-z]', name):
        return False, "Has attached description"

    # Also flag if name ends with lowercase then more words (likely truncated description)
    # But allow legitimate names like CoinFund, HedgeFund, etc.
    if re.search(r'[a-z](Micro|Only|Focused|Category|Integrated|Leverages|Specialized|continental|Deploys)', name):
        return False, "Has attached description"

    # Check for very short names (likely truncated)
    if len(name) <= 4 and not name.isdigit():
        return False, "Name too short"

    # Check for names ending with truncated company suffix
    if name.endswith(' (fk') or name.endswith(' (f/k/') or name.endswith(' (ERA'):
        return False, "Truncated name"

    return True, "Valid"

# Merge: start with curated, then add valid originals not in curated
merged_vcs = list(curated_vcs)
added_from_original = 0
skipped = []

for vc in original_vcs:
    name_lower = vc['name'].lower()

    # Skip if already in curated
    if name_lower in curated_names:
        continue

    # Check if valid
    is_valid, reason = is_valid_vc(vc)
    if is_valid:
        # Add default sector if empty
        if not vc['sectors']:
            vc['sectors'] = ['Technology']
        merged_vcs.append(vc)
        added_from_original += 1
    else:
        skipped.append((vc['name'], reason))

print(f"\nAdded from original: {added_from_original}")
print(f"Skipped: {len(skipped)}")
print(f"Total merged: {len(merged_vcs)}")

# Show what was skipped
print("\nSkipped entries:")
for name, reason in skipped[:30]:
    print(f"  - {name}: {reason}")
if len(skipped) > 30:
    print(f"  ... and {len(skipped) - 30} more")

# Write merged data
def format_vc(vc):
    stages = ', '.join(f'"{s}"' for s in vc['stages'])
    sectors = ', '.join(f'"{s}"' for s in vc['sectors'])
    # Escape quotes in name
    name = vc['name'].replace('"', '\\"')
    location = vc['location'].replace('"', '\\"')
    return f'    {{name:"{name}",location:"{location}",region:"{vc["region"]}",stages:[{stages}],sectors:[{sectors}],check_size:"{vc["check_size"]}",aum:"{vc["aum"]}"}}'

# Sort alphabetically
merged_vcs.sort(key=lambda x: x['name'].lower())

# Remove exact duplicates
seen = set()
unique_vcs = []
for vc in merged_vcs:
    key = vc['name'].lower()
    if key not in seen:
        seen.add(key)
        unique_vcs.append(vc)

print(f"\nAfter dedup: {len(unique_vcs)}")

output = 'const vcData = [\n'
output += ',\n'.join(format_vc(vc) for vc in unique_vcs)
output += '\n];'

with open('data.js', 'w') as f:
    f.write(output)

# Stats
regions = {}
for vc in unique_vcs:
    r = vc['region']
    regions[r] = regions.get(r, 0) + 1

print(f"\nBy region:")
for r, count in sorted(regions.items(), key=lambda x: -x[1]):
    print(f"  {r}: {count}")
