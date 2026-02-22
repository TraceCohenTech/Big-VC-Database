#!/usr/bin/env python3
"""
Add NYC VCs from CSV to the database
"""

import re
import csv

# Read the current data file
with open('data.js', 'r') as f:
    content = f.read()

# Parse existing VCs
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

existing_vcs = parse_vcs(content)
existing_names = {vc['name'].lower() for vc in existing_vcs}

print(f"Current VCs: {len(existing_vcs)}")

# Parse NYC VC CSV
nyc_vcs = {}
with open('/Users/tracecohen/Downloads/NYC VC List - Trace Cohen - NYC VC List.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        if len(row) < 10:
            continue
        firm = row[0].strip()
        if not firm or firm == 'Firm' or firm == 'NYC VC List' or firm == 'Total Firms Listed':
            continue

        fund_size = row[5].strip() if len(row) > 5 else ''
        aum = row[6].strip() if len(row) > 6 else ''
        stages_raw = row[7].strip() if len(row) > 7 else ''
        industries = row[9].strip() if len(row) > 9 else ''

        # Skip if already processed this firm
        if firm in nyc_vcs:
            continue

        # Parse stages
        stages = []
        stages_raw = stages_raw.replace('Seriees', 'Series')  # Fix typo
        if 'Pre-Seed' in stages_raw or 'Pre-seed' in stages_raw:
            stages.append('Pre-Seed')
        if 'Angel' in stages_raw:
            stages.append('Angel')
        if 'Seed' in stages_raw and 'Pre-Seed' not in stages_raw:
            stages.append('Seed')
        if 'Series A' in stages_raw:
            stages.append('Series A')
        if 'Series B' in stages_raw:
            stages.append('Series B')
        if 'Series C' in stages_raw or 'Series D' in stages_raw or 'Series E' in stages_raw:
            stages.append('Growth')
        if 'Growth' in stages_raw or 'Private Equity' in stages_raw:
            stages.append('Growth')
        if 'All' in stages_raw or 'Everything' in stages_raw:
            stages = ['Seed', 'Series A', 'Series B', 'Growth']

        # Remove duplicates
        stages = list(dict.fromkeys(stages))
        if not stages:
            stages = ['Seed', 'Series A']

        # Parse sectors from industries
        sectors = []
        industries_lower = industries.lower()

        if 'fintech' in industries_lower or 'financial' in industries_lower:
            sectors.append('Fintech')
        if 'health' in industries_lower or 'medical' in industries_lower or 'biotech' in industries_lower:
            sectors.append('Healthcare')
        if 'enterprise' in industries_lower or 'saas' in industries_lower or 'b2b' in industries_lower or 'software' in industries_lower:
            sectors.append('Enterprise')
        if 'consumer' in industries_lower or 'e-commerce' in industries_lower or 'ecommerce' in industries_lower or 'retail' in industries_lower:
            sectors.append('Consumer')
        if 'ai' in industries_lower or 'machine learning' in industries_lower or 'artificial intelligence' in industries_lower:
            sectors.append('AI')
        if 'media' in industries_lower or 'entertainment' in industries_lower or 'content' in industries_lower:
            sectors.append('Media')
        if 'crypto' in industries_lower or 'blockchain' in industries_lower or 'web3' in industries_lower:
            sectors.append('Crypto')
        if 'cyber' in industries_lower or 'security' in industries_lower:
            sectors.append('Cybersecurity')
        if 'clean' in industries_lower or 'climate' in industries_lower or 'energy' in industries_lower or 'sustainability' in industries_lower:
            sectors.append('Climate')
        if 'real estate' in industries_lower or 'proptech' in industries_lower:
            sectors.append('Proptech')
        if 'food' in industries_lower or 'beverage' in industries_lower or 'f&b' in industries_lower:
            sectors.append('Foodtech')
        if 'edtech' in industries_lower or 'education' in industries_lower:
            sectors.append('Edtech')
        if 'marketplace' in industries_lower:
            sectors.append('Marketplaces')
        if 'robot' in industries_lower or 'autonomous' in industries_lower or 'drone' in industries_lower:
            sectors.append('Robotics')
        if 'iot' in industries_lower or 'hardware' in industries_lower:
            sectors.append('Hardware')
        if 'mobile' in industries_lower or 'internet' in industries_lower:
            sectors.append('Consumer')
        if 'insur' in industries_lower:
            sectors.append('Insurtech')
        if 'sport' in industries_lower:
            sectors.append('Sports')
        if 'deep tech' in industries_lower or 'frontier' in industries_lower:
            sectors.append('Deeptech')

        # Remove duplicates
        sectors = list(dict.fromkeys(sectors))
        if not sectors:
            sectors = ['Enterprise']

        # Clean AUM
        aum_clean = aum.replace('$', '').replace(',', '').strip()
        if aum_clean and aum_clean.endswith('M'):
            aum_clean = aum_clean
        elif aum_clean:
            try:
                val = float(aum_clean)
                if val >= 1000:
                    aum_clean = f"${val/1000:.1f}B"
                else:
                    aum_clean = f"${val}M"
            except:
                aum_clean = ''

        nyc_vcs[firm] = {
            'name': firm,
            'location': 'New York, NY',
            'region': 'USA',
            'stages': stages,
            'sectors': sectors,
            'check_size': '',
            'aum': aum_clean
        }

print(f"Found {len(nyc_vcs)} unique NYC VCs in CSV")

# Merge new VCs
all_vcs = list(existing_vcs)
added_count = 0
skipped = []

for name, vc in nyc_vcs.items():
    name_lower = name.lower()

    # Skip accelerators and incubators
    if 'accelerator' in name_lower or 'incubator' in name_lower:
        continue

    # Skip if already exists
    if name_lower in existing_names:
        skipped.append(name)
        continue

    # Skip some edge cases
    if name_lower in ['jj kasper', 'joe robinson', 'john ason', 'judson cooper', 'mark gerson', 'nisa amoils']:
        continue  # Individual angels, not firms

    all_vcs.append(vc)
    existing_names.add(name_lower)
    added_count += 1
    print(f"Added: {name}")

print(f"\n{'='*50}")
print(f"Added: {added_count} NYC VCs")
print(f"Skipped (already exist): {len(skipped)}")
print(f"Total: {len(all_vcs)}")

# Write updated data
def format_vc(vc):
    stages = ', '.join(f'"{s}"' for s in vc['stages'])
    sectors = ', '.join(f'"{s}"' for s in vc['sectors'])
    name = vc['name'].replace('"', '\\"')
    location = vc['location'].replace('"', '\\"')
    return f'    {{name:"{name}",location:"{location}",region:"{vc["region"]}",stages:[{stages}],sectors:[{sectors}],check_size:"{vc["check_size"]}",aum:"{vc["aum"]}"}}'

# Sort alphabetically
all_vcs.sort(key=lambda x: x['name'].lower())

# Remove duplicates
seen = set()
unique_vcs = []
for vc in all_vcs:
    key = vc['name'].lower()
    if key not in seen:
        seen.add(key)
        unique_vcs.append(vc)

print(f"After dedup: {len(unique_vcs)}")

output = 'const vcData = [\n'
output += ',\n'.join(format_vc(vc) for vc in unique_vcs)
output += '\n];'

with open('data.js', 'w') as f:
    f.write(output)

# Print stats
regions = {}
for vc in unique_vcs:
    r = vc['region']
    regions[r] = regions.get(r, 0) + 1

print(f"\nBy region:")
for r, count in sorted(regions.items(), key=lambda x: -x[1]):
    print(f"  {r}: {count}")

print(f"\nUpdated data.js with {len(unique_vcs)} VCs")
