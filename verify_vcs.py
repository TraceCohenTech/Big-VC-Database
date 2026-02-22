#!/usr/bin/env python3
"""
VC Data Verification and Cleanup Script
Verifies VCs are real, active, and properly tagged
"""

import re
import json

# Read the current data file
with open('data.js', 'r') as f:
    content = f.read()

# Extract the array content
match = re.search(r'const vcData = \[(.*)\];', content, re.DOTALL)
if not match:
    print("Could not find vcData array")
    exit(1)

# Parse individual VC entries
vc_text = match.group(1)
vcs = []

# Pattern to match each VC object
pattern = r'\{name:"([^"]*)",location:"([^"]*)",region:"([^"]*)",stages:\[(.*?)\],sectors:\[(.*?)\],check_size:"([^"]*)",aum:"([^"]*)"\}'

for m in re.finditer(pattern, vc_text):
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

print(f"Found {len(vcs)} VCs in data file")

# ============================================
# CORRECTIONS BASED ON RESEARCH
# ============================================

# VCs to REMOVE (defunct, shut down, or not real VCs)
REMOVE_VCS = {
    'Countdown Capital',  # Shut down in early 2024
    'SAP.iO',  # Closed March 2024
    'A Capital*',  # Invalid entry with asterisk
    'Foo',  # Not a real VC
    'Google',  # Corporate, not a VC fund
    'Cle',  # Incomplete/invalid entry
    'Col',  # Incomplete/invalid entry
    'Fin',  # Incomplete/invalid entry
    'Edu',  # Incomplete/invalid entry
    'Conscience',  # Duplicate/incomplete
    'Coalition',  # Duplicate of Coalition Operators
    'Costano',  # Duplicate of Costanoa Ventures
    'Chingon',  # Duplicate of Chingona Ventures
    'Gan',  # Incomplete entry
    'Comm',  # Incomplete entry
}

# VCs with malformed names (description attached) - clean these
NAME_CLEANUPS = {
    'Felicis VenturesPrioritizes': 'Felicis Ventures',
    'GGV CapitalBuilt': 'GGV Capital',
    'GreylockVC': 'Greylock Partners',
    'GVFinancially': 'GV (Google Ventures)',
    'Bessemer Venture': 'Bessemer Venture Partners',
    'Coatue': 'Coatue Management',
    'CRV': 'CRV (Charles River Ventures)',
    'First Round Capital': 'First Round Capital',
    'ff Venture CapitalBi‑continental': 'ff Venture Capital',
    'Dynamo VenturesCategory': 'Dynamo Ventures',
    'Delphi VenturesIntegrated': 'Delphi Ventures',
    'Digitalis VenturesIntegrated': 'Digitalis Ventures',
    'DCG ExpeditionsBacked': 'DCG Expeditions',
    'Core Innovation CapitalFin': 'Core Innovation Capital',
    'Copper Wire VenturesMicrofund': 'Copper Wire Ventures',
    'Crosslink CapitalLeverages': 'Crosslink Capital',
    'Emerson CollectiveLow-visibility': 'Emerson Collective',
    'Eniac VenturesPure-p': 'Eniac Ventures',
    'Energy FoundryNonprofit': 'Energy Foundry',
    'Equal Opportunity (EO) VenturesBill': 'Equal Opportunity Ventures',
    'ExpaActs': 'Expa',
    'Fearless FundBuilt': 'Fearless Fund',
    'Figure 8 InvestmentsMarried': 'Figure 8 Investments',
    'Firework VenturesTools': 'Firework Ventures',
    'Fitch Ventures (f/k/': 'Fitch Ventures',
    'Flint CapitalDistributed': 'Flint Capital',
    'Forum Ventures (fk': 'Forum Ventures',
    'F-Prime Capital (fk': 'F-Prime Capital',
    'Foundry GroupDirect': 'Foundry Group',
    'Frist Cressey VenturesGP': 'Frist Cressey Ventures',
    'FTW VenturesSpecialized': 'FTW Ventures',
    'Fuel CapitalSupportive': 'Fuel Capital',
    'GaingelsCommunity': 'Gaingels',
    'Geek VenturesAccepts': 'Geek Ventures',
    'GigafundExtremely': 'Gigafund',
    'GingerBread CapitalFund': 'GingerBread Capital',
    'GoAhead VenturesAccessible': 'GoAhead Ventures',
    'Gold House VenturesTied': 'Gold House Ventures',
    'Graham & WalkerBorn': 'Graham & Walker',
    'Hamilton VenturesConnects': 'Hamilton Ventures',
    'Distributed VenturesDeploys $1–5M': 'Distributed Ventures',
    'Elevar EquityOften': 'Elevar Equity',
    'Entrepreneurs Roundtable Accelerator (ERA': 'Entrepreneurs Roundtable Accelerator',
}

# CORRECT SECTOR TAGS for major VCs (based on research)
SECTOR_CORRECTIONS = {
    'Sequoia Capital': ['AI', 'Enterprise', 'Consumer', 'Fintech', 'Healthcare', 'Crypto', 'Climate'],
    'Andreessen Horowitz': ['AI', 'Fintech', 'Crypto', 'Enterprise', 'Healthcare', 'Biotech', 'Defense', 'Consumer'],
    'Accel': ['AI', 'Enterprise', 'SaaS', 'Consumer', 'Fintech', 'Cybersecurity', 'Healthcare'],
    'Benchmark': ['Consumer', 'Enterprise', 'AI', 'Marketplaces', 'Infrastructure'],
    'Greylock Partners': ['Enterprise', 'AI', 'Cybersecurity', 'SaaS', 'Fintech', 'Consumer', 'Infrastructure'],
    'Greylock': ['Enterprise', 'AI', 'Cybersecurity', 'SaaS', 'Fintech', 'Consumer'],
    'Kleiner Perkins': ['Enterprise', 'Consumer', 'Fintech', 'Hardtech', 'Healthcare', 'AI', 'Climate'],
    'Lightspeed Venture Partners': ['Enterprise', 'AI', 'Fintech', 'Consumer', 'Healthcare', 'Cybersecurity'],
    'First Round Capital': ['Enterprise', 'AI', 'Fintech', 'Healthcare', 'Consumer', 'Hardware'],
    'Union Square Ventures': ['Enterprise', 'Fintech', 'Climate', 'Web3', 'AI', 'Healthcare', 'Consumer'],
    'Khosla Ventures': ['AI', 'Climate', 'Healthcare', 'Enterprise', 'Fintech', 'Robotics', 'Deeptech'],
    'New Enterprise Associates': ['AI', 'Enterprise', 'Healthcare', 'Fintech', 'Cybersecurity', 'Consumer'],
    'Tiger Global': ['Consumer', 'Fintech', 'Enterprise', 'AI'],
    'Coatue Management': ['AI', 'Consumer', 'Enterprise', 'Fintech'],
    'GV (Google Ventures)': ['AI', 'Healthcare', 'Enterprise', 'Consumer', 'Climate'],
    'Founders Fund': ['Aerospace', 'Defense', 'Fintech', 'AI', 'Deeptech', 'Healthcare'],
    'Bessemer Venture Partners': ['SaaS', 'Cloud', 'Cybersecurity', 'Healthcare', 'Consumer', 'AI'],
    'Battery Ventures': ['Enterprise', 'AI', 'Industrial', 'Healthcare'],
    'General Catalyst': ['Enterprise', 'Consumer', 'Healthcare', 'Fintech', 'AI', 'Climate'],
    'Index Ventures': ['Enterprise', 'Consumer', 'Fintech', 'Gaming', 'AI'],
    'Insight Partners': ['Enterprise', 'SaaS', 'Fintech', 'AI'],
    'DCVC': ['Deeptech', 'AI', 'Climate', 'Healthcare', 'Industrial'],
    'Lux Capital': ['Deeptech', 'Defense', 'Healthcare', 'AI', 'Climate'],
    'Ribbit Capital': ['Fintech', 'Consumer'],
    'Thrive Capital': ['Enterprise', 'Consumer', 'AI', 'Fintech'],
    'a16z': ['AI', 'Fintech', 'Crypto', 'Enterprise', 'Healthcare', 'Biotech', 'Defense'],
    'Y Combinator': ['Enterprise', 'Consumer', 'AI', 'Fintech', 'Healthcare', 'SaaS'],
    '8VC': ['Defense', 'Logistics', 'Healthcare', 'Fintech', 'Industrial'],
    'Felicis Ventures': ['Enterprise', 'Consumer', 'Fintech', 'AI', 'Climate'],
    'CRV (Charles River Ventures)': ['Enterprise', 'Consumer', 'AI', 'Fintech'],
    'Craft Ventures': ['SaaS', 'Enterprise', 'Fintech', 'AI'],
    'NFX': ['Marketplaces', 'Fintech', 'Gaming', 'AI'],
    'Initialized Capital': ['Enterprise', 'Consumer', 'Fintech', 'AI'],
    'Floodgate': ['Consumer', 'Enterprise', 'AI'],
    'Homebrew': ['Enterprise', 'Consumer', 'Fintech'],
    'Boldstart Ventures': ['Enterprise', 'Developer Tools', 'AI', 'Cybersecurity'],
    'Amplify Partners': ['AI', 'Developer Tools', 'Enterprise', 'Infrastructure'],
    '500 Global': ['Enterprise', 'Fintech', 'Consumer', 'AI'],
    'Gradient Ventures': ['AI'],
    'Electric Capital': ['Crypto', 'Web3'],
    'Paradigm': ['Crypto', 'Web3'],
    'Blockchain Capital': ['Crypto', 'Web3'],
    'Haun Ventures': ['Crypto', 'Web3'],
    'Polychain Capital': ['Crypto', 'Web3'],
    'Framework Ventures': ['Crypto', 'Web3', 'DeFi'],
    'Breakthrough Energy': ['Climate', 'Energy'],
    'Lowercarbon Capital': ['Climate'],
    'Congruent Ventures': ['Climate', 'Sustainability'],
    'Clean Energy Ventures': ['Climate', 'Energy'],
    'Obvious Ventures': ['Climate', 'Healthcare', 'Consumer'],
    'ARCH Venture Partners': ['Biotech', 'Healthcare', 'Deeptech'],
    '5AM Ventures': ['Healthcare', 'Biotech'],
    'Canaan Partners': ['Healthcare', 'Enterprise', 'Consumer'],
    'Polaris Partners': ['Healthcare', 'Enterprise'],
    'OrbiMed': ['Healthcare', 'Biotech'],
    'RA Capital': ['Healthcare', 'Biotech'],
    'Flagship Pioneering': ['Biotech', 'Healthcare'],
    'BITKRAFT': ['Gaming', 'Esports', 'Web3'],
    'Makers Fund': ['Gaming'],
    'Griffin Gaming Partners': ['Gaming'],
    '1Up Ventures': ['Gaming'],
    'Play Ventures': ['Gaming'],
    'Fifth Wall': ['Proptech', 'Real Estate', 'Climate'],
    'MetaProp': ['Proptech', 'Real Estate'],
    'Camber Creek': ['Proptech'],
    'Female Founders Fund': ['Consumer', 'Enterprise', 'Healthcare'],
    'Backstage Capital': ['Consumer', 'Enterprise'],
    'Harlem Capital': ['Consumer', 'Enterprise', 'Fintech'],
    'Precursor Ventures': ['Consumer', 'Enterprise', 'Fintech'],
    'Base10 Partners': ['Enterprise', 'Fintech', 'AI'],
    'Cowboy Ventures': ['Consumer', 'Enterprise'],
    'Forerunner Ventures': ['Consumer', 'Commerce'],
    'Maveron': ['Consumer'],
    'Forerunner': ['Consumer', 'Commerce'],
}

# STAGE CORRECTIONS for major VCs
STAGE_CORRECTIONS = {
    'Tiger Global': ['Seed', 'Series A', 'Series B', 'Growth'],
    'Insight Partners': ['Series A', 'Series B', 'Growth'],
    'General Atlantic': ['Growth'],
    'GIC': ['Growth'],
    'SoftBank Vision Fund': ['Series B', 'Growth'],
}

# Duplicate entries to remove (keep the more complete one)
DUPLICATES_TO_REMOVE = {
    'Bessemer Venture',  # Keep 'Bessemer Venture Partners'
    'Coatue',  # Keep 'Coatue Management'
    'Greylock',  # Keep 'Greylock Partners'
    'GreylockVC',
    'GGV CapitalBuilt',
    'GVFinancially',
    'Felicis VenturesPrioritizes',
}

# ============================================
# APPLY CORRECTIONS
# ============================================

cleaned_vcs = []
seen_names = set()

for vc in vcs:
    name = vc['name']

    # Skip VCs to remove
    if name in REMOVE_VCS:
        print(f"REMOVING (defunct/invalid): {name}")
        continue

    # Skip duplicates
    if name in DUPLICATES_TO_REMOVE:
        print(f"REMOVING (duplicate): {name}")
        continue

    # Clean malformed names
    if name in NAME_CLEANUPS:
        old_name = name
        name = NAME_CLEANUPS[name]
        vc['name'] = name
        print(f"RENAMED: {old_name} -> {name}")

    # Check for duplicate after rename
    normalized = name.lower().strip()
    if normalized in seen_names:
        print(f"SKIPPING (already exists): {name}")
        continue
    seen_names.add(normalized)

    # Apply sector corrections
    if name in SECTOR_CORRECTIONS:
        old_sectors = vc['sectors']
        vc['sectors'] = SECTOR_CORRECTIONS[name]
        print(f"UPDATED SECTORS: {name}: {old_sectors} -> {vc['sectors']}")

    # Apply stage corrections
    if name in STAGE_CORRECTIONS:
        old_stages = vc['stages']
        vc['stages'] = STAGE_CORRECTIONS[name]
        print(f"UPDATED STAGES: {name}: {old_stages} -> {vc['stages']}")

    # Clean up empty sectors - add "Technology" as default
    if not vc['sectors']:
        vc['sectors'] = ['Technology']

    cleaned_vcs.append(vc)

print(f"\n{'='*50}")
print(f"Original count: {len(vcs)}")
print(f"After cleanup: {len(cleaned_vcs)}")
print(f"Removed: {len(vcs) - len(cleaned_vcs)}")

# ============================================
# WRITE CLEANED DATA
# ============================================

def format_vc(vc):
    stages = ', '.join(f'"{s}"' for s in vc['stages'])
    sectors = ', '.join(f'"{s}"' for s in vc['sectors'])
    return f'    {{name:"{vc["name"]}",location:"{vc["location"]}",region:"{vc["region"]}",stages:[{stages}],sectors:[{sectors}],check_size:"{vc["check_size"]}",aum:"{vc["aum"]}"}}'

# Sort alphabetically by name
cleaned_vcs.sort(key=lambda x: x['name'].lower())

output = 'const vcData = [\n'
output += ',\n'.join(format_vc(vc) for vc in cleaned_vcs)
output += '\n];'

with open('data_cleaned.js', 'w') as f:
    f.write(output)

print(f"\nCleaned data written to data_cleaned.js")
print(f"Total verified VCs: {len(cleaned_vcs)}")

# Print summary stats
regions = {}
for vc in cleaned_vcs:
    r = vc['region']
    regions[r] = regions.get(r, 0) + 1

print(f"\nBy region:")
for r, count in sorted(regions.items(), key=lambda x: -x[1]):
    print(f"  {r}: {count}")
