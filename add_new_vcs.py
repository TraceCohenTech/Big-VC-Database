#!/usr/bin/env python3
"""
Add new VCs to the database from research sources including vcdir.com
"""

import re

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

# Israeli VCs from vcdir.com and other research sources
NEW_ISRAELI_VCS = [
    # From vcdir.com Israel page
    {"name": "Amiti Ventures", "location": "Tel Aviv, Israel", "stages": ["Seed", "Series A"], "sectors": ["Deeptech", "Quantum", "Biotech", "Cybersecurity", "Semiconductors"], "check_size": "$1M-$10M", "aum": ""},
    {"name": "aMoon", "location": "Ra'anana, Israel", "stages": ["Seed", "Series A", "Series B", "Series C"], "sectors": ["Healthcare", "Biotech"], "check_size": "$5M-$50M", "aum": "$1B"},
    {"name": "Awz Ventures", "location": "Tel Aviv, Israel", "stages": ["Pre-Seed", "Seed", "Series A", "Series B"], "sectors": ["Cybersecurity", "AI", "Medtech", "Quantum"], "check_size": "$500K-$10M", "aum": ""},
    {"name": "Benhamou Global Ventures", "location": "Tel Aviv, Israel", "stages": ["Series A", "Series B"], "sectors": ["Enterprise", "AI"], "check_size": "$2M-$15M", "aum": ""},
    {"name": "Claltech", "location": "Tel Aviv, Israel", "stages": ["Series B", "Growth"], "sectors": ["Consumer", "Enterprise"], "check_size": "$5M-$50M", "aum": ""},
    {"name": "Deep Insight", "location": "Herzliya, Israel", "stages": ["Series A", "Series B", "Series C"], "sectors": ["Semiconductors", "Biotech", "Robotics"], "check_size": "$5M-$25M", "aum": ""},
    {"name": "DRW Venture Capital", "location": "Tel Aviv, Israel", "stages": ["Series A", "Series B", "Series C"], "sectors": ["Fintech", "Enterprise"], "check_size": "$5M-$30M", "aum": ""},
    {"name": "Flashpoint", "location": "Tel Aviv, Israel", "stages": ["Seed", "Series A"], "sectors": ["Enterprise", "SaaS"], "check_size": "$1M-$10M", "aum": ""},
    {"name": "Genesis Partners", "location": "Herzliya, Israel", "stages": ["Seed", "Series A", "Series B", "Series C"], "sectors": ["SaaS", "AI", "Enterprise", "Consumer"], "check_size": "$1M-$20M", "aum": "$700M"},
    {"name": "Hearst Ventures Israel", "location": "Tel Aviv, Israel", "stages": ["Series A", "Series B", "Series C"], "sectors": ["Media", "Fintech", "Enterprise", "AI"], "check_size": "$1M-$15M", "aum": ""},
    {"name": "Innovation Endeavors", "location": "Tel Aviv, Israel", "stages": ["Seed", "Series A", "Series B", "Series C"], "sectors": ["AI", "Healthcare", "Enterprise"], "check_size": "$1M-$30M", "aum": "$1B"},
    {"name": "InMotion Ventures", "location": "Tel Aviv, Israel", "stages": ["Seed", "Series A", "Series B"], "sectors": ["Climate", "Industrial", "Enterprise"], "check_size": "$1M-$15M", "aum": ""},
    {"name": "Corundum Neuroscience", "location": "Herzliya, Israel", "stages": ["Seed", "Series A"], "sectors": ["Healthcare", "Biotech"], "check_size": "$500K-$5M", "aum": ""},
    {"name": "Key1 Capital", "location": "Herzliya, Israel", "stages": ["Series A", "Series B", "Series C"], "sectors": ["Enterprise", "Fintech", "Cybersecurity"], "check_size": "$5M-$30M", "aum": ""},
    {"name": "LionBird", "location": "Tel Aviv, Israel", "stages": ["Pre-Seed", "Seed", "Series A"], "sectors": ["Healthcare", "AI"], "check_size": "$500K-$5M", "aum": ""},
    {"name": "Maor Investments", "location": "Tel Aviv, Israel", "stages": ["Series B", "Growth"], "sectors": ["SaaS", "AI", "Cybersecurity", "Healthcare", "Commerce"], "check_size": "$5M-$50M", "aum": ""},
    {"name": "PeakBridge VC", "location": "Tel Aviv, Israel", "stages": ["Seed", "Series A", "Series B"], "sectors": ["Foodtech", "Agtech", "Climate"], "check_size": "$1M-$10M", "aum": ""},
    {"name": "Surround Ventures", "location": "Tel Aviv, Israel", "stages": ["Seed", "Series A"], "sectors": ["Media", "Entertainment", "Commerce"], "check_size": "$500K-$5M", "aum": ""},
    {"name": "Longliv Ventures", "location": "Herzliya, Israel", "stages": ["Series A", "Series B", "Series C"], "sectors": ["Healthcare", "Medtech"], "check_size": "$3M-$20M", "aum": ""},

    # Additional Israeli VCs from research
    {"name": "Magma Venture Partners", "location": "Tel Aviv, Israel", "stages": ["Seed", "Series A", "Series B"], "sectors": ["Enterprise", "Semiconductors", "AI"], "check_size": "$1M-$10M", "aum": "$600M"},
    {"name": "Hanaco Venture Capital", "location": "Tel Aviv, Israel", "stages": ["Seed", "Series A", "Series B"], "sectors": ["Enterprise", "Consumer"], "check_size": "$2M-$100M", "aum": "$1.5B"},
    {"name": "FinTLV", "location": "Tel Aviv, Israel", "stages": ["Seed", "Series A"], "sectors": ["Fintech", "Insurtech"], "check_size": "$1M-$10M", "aum": "$200M"},
    {"name": "Pontifax", "location": "Herzliya, Israel", "stages": ["Seed", "Series A", "Series B", "Growth"], "sectors": ["Healthcare", "Biotech"], "check_size": "$1M-$50M", "aum": "$1B"},
    {"name": "Lool Ventures", "location": "Tel Aviv, Israel", "stages": ["Seed", "Series A"], "sectors": ["Enterprise", "AI", "Healthcare", "Fintech"], "check_size": "$500K-$3M", "aum": "$180M"},
    {"name": "Gemini Israel Ventures", "location": "Herzliya, Israel", "stages": ["Seed", "Series A", "Series B", "Series C"], "sectors": ["Enterprise", "Digital Media", "Semiconductors"], "check_size": "$500K-$15M", "aum": "$650M"},
    {"name": "Cardumen Capital", "location": "Tel Aviv, Israel", "stages": ["Pre-Seed", "Seed", "Series A"], "sectors": ["Deeptech", "Agtech", "AI"], "check_size": "$500K-$5M", "aum": "$100M"},
    {"name": "S Capital", "location": "Tel Aviv, Israel", "stages": ["Seed", "Series A"], "sectors": ["AI", "Deeptech", "Cybersecurity", "Fintech"], "check_size": "$1M-$5M", "aum": "$250M"},
    {"name": "10D", "location": "Tel Aviv, Israel", "stages": ["Seed", "Series A"], "sectors": ["Logistics", "Supply Chain"], "check_size": "$500K-$5M", "aum": "$150M"},
    {"name": "Hetz Ventures", "location": "Tel Aviv, Israel", "stages": ["Seed", "Series A"], "sectors": ["Deeptech", "Developer Tools", "Cybersecurity", "AI"], "check_size": "$500K-$5M", "aum": "$123M"},
    {"name": "F2 Venture Capital", "location": "Tel Aviv, Israel", "stages": ["Pre-Seed", "Seed"], "sectors": ["AI", "Cybersecurity", "Fintech", "Cloud"], "check_size": "$500K-$4M", "aum": "$250M"},
    {"name": "AltaIR Capital", "location": "Herzliya, Israel", "stages": ["Pre-Seed", "Seed"], "sectors": ["Consumer", "Mobile"], "check_size": "$100K-$3M", "aum": "$100M"},
    {"name": "MizMaa Ventures", "location": "Tel Aviv, Israel", "stages": ["Seed", "Series A"], "sectors": ["Deeptech", "AI"], "check_size": "$1M-$5M", "aum": "$150M"},
    {"name": "Magenta Venture Partners", "location": "Herzliya, Israel", "stages": ["Series A"], "sectors": ["Automotive", "Mobility", "Enterprise", "AI"], "check_size": "$2M-$10M", "aum": "$150M"},
    {"name": "Giza Venture Capital", "location": "Tel Aviv, Israel", "stages": ["Seed", "Series A"], "sectors": ["Enterprise", "Deeptech"], "check_size": "$1M-$10M", "aum": "$500M"},
    {"name": "StageOne Ventures", "location": "Tel Aviv, Israel", "stages": ["Seed", "Series A"], "sectors": ["Enterprise", "AI", "Healthcare"], "check_size": "$500K-$5M", "aum": "$200M"},
    {"name": "Viola Growth", "location": "Herzliya, Israel", "stages": ["Series B", "Growth"], "sectors": ["Enterprise", "Consumer"], "check_size": "$10M-$100M", "aum": "$1.5B"},
    {"name": "Peregrine Ventures", "location": "Or Yehuda, Israel", "stages": ["Seed", "Series A", "Series B"], "sectors": ["Healthcare", "Enterprise"], "check_size": "$1M-$15M", "aum": "$400M"},
    {"name": "Vintage Investment Partners", "location": "Tel Aviv, Israel", "stages": ["Seed", "Series A", "Series B", "Growth"], "sectors": ["Enterprise", "Consumer"], "check_size": "$5M-$50M", "aum": "$3B"},
    {"name": "MoreVC", "location": "Ra'anana, Israel", "stages": ["Seed", "Series A"], "sectors": ["Enterprise", "Consumer"], "check_size": "$500K-$5M", "aum": "$150M"},
    {"name": "Cedar Fund", "location": "Herzliya, Israel", "stages": ["Seed", "Series A"], "sectors": ["Enterprise", "AI"], "check_size": "$500K-$3M", "aum": "$100M"},
    {"name": "Remagine Ventures", "location": "Tel Aviv, Israel", "stages": ["Seed", "Series A"], "sectors": ["Consumer", "Commerce", "Entertainment"], "check_size": "$500K-$3M", "aum": "$150M"},
    {"name": "Crescendo Venture Partners", "location": "Tel Aviv, Israel", "stages": ["Seed", "Series A", "Series B"], "sectors": ["Enterprise", "AI", "SaaS"], "check_size": "$1M-$10M", "aum": "$200M"},
    {"name": "iAngels", "location": "Tel Aviv, Israel", "stages": ["Seed", "Series A"], "sectors": ["Enterprise", "Healthcare", "AI"], "check_size": "$100K-$3M", "aum": "$500M"},
    {"name": "Maniv Mobility", "location": "Tel Aviv, Israel", "stages": ["Seed", "Series A"], "sectors": ["Mobility", "Robotics", "Automotive"], "check_size": "$500K-$5M", "aum": "$100M"},
    {"name": "Target Global", "location": "Tel Aviv, Israel", "stages": ["Seed", "Series A", "Series B", "Growth"], "sectors": ["Fintech", "Enterprise", "Consumer"], "check_size": "$1M-$100M", "aum": "$3B"},
    {"name": "INcapital Ventures", "location": "Tel Aviv, Israel", "stages": ["Series A", "Series B"], "sectors": ["AI", "IoT", "Cybersecurity", "Fintech"], "check_size": "$1M-$10M", "aum": "$100M"},
    {"name": "State of Mind Ventures", "location": "Tel Aviv, Israel", "stages": ["Pre-Seed", "Seed"], "sectors": ["Enterprise", "Consumer"], "check_size": "$250K-$2M", "aum": "$50M"},
    {"name": "Firstime Ventures", "location": "Tel Aviv, Israel", "stages": ["Seed", "Series A"], "sectors": ["Enterprise", "AI"], "check_size": "$500K-$5M", "aum": "$150M"},
    {"name": "Alon Medtech Ventures", "location": "Tel Aviv, Israel", "stages": ["Seed", "Series A"], "sectors": ["Healthcare", "Medtech"], "check_size": "$1M-$10M", "aum": "$200M"},
    {"name": "TAU Ventures", "location": "Tel Aviv, Israel", "stages": ["Pre-Seed", "Seed"], "sectors": ["Enterprise", "AI", "Deeptech"], "check_size": "$250K-$1M", "aum": "$30M"},
    {"name": "Pico Partners", "location": "Tel Aviv, Israel", "stages": ["Seed", "Series A"], "sectors": ["Enterprise", "Consumer", "AI"], "check_size": "$500K-$5M", "aum": "$100M"},
    {"name": "Champel Capital", "location": "Tel Aviv, Israel", "stages": ["Seed", "Series A"], "sectors": ["Enterprise", "Fintech"], "check_size": "$1M-$10M", "aum": "$200M"},
    {"name": "VC23", "location": "Tel Aviv, Israel", "stages": ["Pre-Seed", "Seed"], "sectors": ["Enterprise", "Consumer"], "check_size": "$100K-$1M", "aum": "$30M"},
    {"name": "NextLeap Ventures", "location": "Tel Aviv, Israel", "stages": ["Seed", "Series A"], "sectors": ["Enterprise", "AI"], "check_size": "$500K-$5M", "aum": "$80M"},
    {"name": "Elron Ventures", "location": "Tel Aviv, Israel", "stages": ["Seed", "Series A", "Series B"], "sectors": ["Enterprise", "Healthcare", "Cybersecurity"], "check_size": "$1M-$15M", "aum": "$300M"},
    {"name": "Planven Entrepreneur Ventures", "location": "Tel Aviv, Israel", "stages": ["Series A", "Series B"], "sectors": ["Enterprise", "Consumer"], "check_size": "$5M-$20M", "aum": "$200M"},
    {"name": "Capri Ventures", "location": "Tel Aviv, Israel", "stages": ["Seed", "Series A"], "sectors": ["Consumer", "Retail", "Foodtech"], "check_size": "$500K-$5M", "aum": "$100M"},
    {"name": "Vertex Ventures HC", "location": "Tel Aviv, Israel", "stages": ["Seed", "Series A", "Series B"], "sectors": ["Healthcare", "Biotech", "Medtech"], "check_size": "$1M-$20M", "aum": "$500M"},
]

# New US VCs
NEW_US_VCS = [
    {"name": "Hyde Park Venture Partners", "location": "Chicago, IL", "stages": ["Seed", "Series A"], "sectors": ["Enterprise", "SaaS"], "check_size": "$500K-$7M", "aum": "$200M"},
    {"name": "M13", "location": "Los Angeles, CA", "stages": ["Seed", "Series A", "Series B"], "sectors": ["Consumer", "Enterprise", "Fintech"], "check_size": "$1M-$25M", "aum": "$1B"},
    {"name": "SignalFire", "location": "San Francisco, CA", "stages": ["Seed", "Series A", "Series B"], "sectors": ["Enterprise", "AI", "Consumer"], "check_size": "$1M-$30M", "aum": "$2B"},
    {"name": "Uncork Capital", "location": "San Francisco, CA", "stages": ["Seed", "Series A"], "sectors": ["Enterprise", "SaaS"], "check_size": "$1M-$7M", "aum": "$700M"},
    {"name": "Blumberg Capital", "location": "San Francisco, CA", "stages": ["Seed", "Series A", "Series B"], "sectors": ["Enterprise", "Fintech", "Cybersecurity"], "check_size": "$500K-$15M", "aum": "$500M"},
    {"name": "Norwest Venture Partners", "location": "Menlo Park, CA", "stages": ["Series A", "Series B", "Growth"], "sectors": ["Enterprise", "Healthcare", "Consumer"], "check_size": "$5M-$100M", "aum": "$15B"},
    {"name": "Drive Capital", "location": "Columbus, OH", "stages": ["Seed", "Series A", "Series B"], "sectors": ["Enterprise", "Consumer"], "check_size": "$1M-$25M", "aum": "$1B"},
    {"name": "Tribe Capital", "location": "San Francisco, CA", "stages": ["Seed", "Series A", "Series B", "Growth"], "sectors": ["Enterprise", "Consumer", "Fintech"], "check_size": "$1M-$100M", "aum": "$1.5B"},
    {"name": "Inspired Capital", "location": "New York, NY", "stages": ["Seed", "Series A"], "sectors": ["Enterprise", "Consumer"], "check_size": "$1M-$15M", "aum": "$400M"},
    {"name": "Work-Bench", "location": "New York, NY", "stages": ["Seed", "Series A"], "sectors": ["Enterprise", "SaaS"], "check_size": "$1M-$5M", "aum": "$200M"},
    {"name": "Accomplice", "location": "Boston, MA", "stages": ["Seed", "Series A"], "sectors": ["Enterprise", "Consumer"], "check_size": "$500K-$5M", "aum": "$500M"},
    {"name": "Primary Venture Partners", "location": "New York, NY", "stages": ["Seed", "Series A"], "sectors": ["Consumer", "Enterprise"], "check_size": "$500K-$10M", "aum": "$500M"},
    {"name": "Equal Ventures", "location": "New York, NY", "stages": ["Seed", "Series A"], "sectors": ["Fintech", "Healthcare", "Enterprise"], "check_size": "$500K-$5M", "aum": "$200M"},
    {"name": "Flybridge", "location": "Boston, MA", "stages": ["Seed", "Series A"], "sectors": ["Enterprise", "Healthcare"], "check_size": "$500K-$10M", "aum": "$500M"},
    {"name": "Venrock", "location": "Palo Alto, CA", "stages": ["Seed", "Series A", "Series B"], "sectors": ["Healthcare", "Enterprise", "AI"], "check_size": "$1M-$30M", "aum": "$3B"},
    {"name": "Northzone", "location": "New York, NY", "stages": ["Seed", "Series A", "Series B"], "sectors": ["Enterprise", "Consumer", "Fintech"], "check_size": "$1M-$50M", "aum": "$2B"},
    {"name": "Greycroft", "location": "New York, NY", "stages": ["Seed", "Series A", "Series B"], "sectors": ["Consumer", "Enterprise", "Healthcare"], "check_size": "$1M-$25M", "aum": "$2B"},
    {"name": "Tenaya Capital", "location": "Menlo Park, CA", "stages": ["Series A", "Series B"], "sectors": ["Enterprise", "Healthcare"], "check_size": "$5M-$50M", "aum": "$2B"},
    {"name": "Madrona Ventures", "location": "Seattle, WA", "stages": ["Seed", "Series A", "Series B"], "sectors": ["Enterprise", "AI", "Cloud"], "check_size": "$1M-$20M", "aum": "$3B"},
    {"name": "Sapphire Ventures", "location": "Palo Alto, CA", "stages": ["Series A", "Series B", "Growth"], "sectors": ["Enterprise", "SaaS"], "check_size": "$5M-$100M", "aum": "$10B"},
    {"name": "Redpoint Ventures", "location": "Menlo Park, CA", "stages": ["Seed", "Series A", "Series B", "Growth"], "sectors": ["Enterprise", "Consumer", "Infrastructure"], "check_size": "$1M-$100M", "aum": "$6B"},
    {"name": "Scale Venture Partners", "location": "Foster City, CA", "stages": ["Series A", "Series B"], "sectors": ["Enterprise", "SaaS"], "check_size": "$5M-$50M", "aum": "$2B"},
    {"name": "IVP", "location": "Menlo Park, CA", "stages": ["Series A", "Series B", "Growth"], "sectors": ["Enterprise", "Consumer"], "check_size": "$10M-$100M", "aum": "$10B"},
    {"name": "Emergence Capital", "location": "San Francisco, CA", "stages": ["Series A", "Series B"], "sectors": ["Enterprise", "SaaS"], "check_size": "$5M-$30M", "aum": "$3B"},
    {"name": "Iconiq Capital", "location": "San Francisco, CA", "stages": ["Series A", "Series B", "Growth"], "sectors": ["Enterprise", "Consumer"], "check_size": "$5M-$100M", "aum": "$80B"},
    {"name": "Storm Ventures", "location": "Menlo Park, CA", "stages": ["Seed", "Series A"], "sectors": ["Enterprise", "SaaS"], "check_size": "$500K-$10M", "aum": "$500M"},
    {"name": "Costanoa Ventures", "location": "Palo Alto, CA", "stages": ["Seed", "Series A"], "sectors": ["Enterprise", "AI"], "check_size": "$500K-$10M", "aum": "$700M"},
    {"name": "Hustle Fund", "location": "San Francisco, CA", "stages": ["Pre-Seed", "Seed"], "sectors": ["Enterprise", "Consumer"], "check_size": "$25K-$500K", "aum": "$100M"},
    {"name": "Chapter One", "location": "San Francisco, CA", "stages": ["Pre-Seed", "Seed"], "sectors": ["Enterprise", "Consumer"], "check_size": "$100K-$1M", "aum": "$200M"},
    {"name": "Village Global", "location": "San Francisco, CA", "stages": ["Pre-Seed", "Seed"], "sectors": ["Enterprise", "Consumer", "AI"], "check_size": "$100K-$500K", "aum": "$300M"},
    {"name": "Revolution Ventures", "location": "Washington, DC", "stages": ["Seed", "Series A", "Series B"], "sectors": ["Enterprise", "Consumer"], "check_size": "$1M-$25M", "aum": "$500M"},
    {"name": "Revolution Rise of the Rest", "location": "Washington, DC", "stages": ["Seed", "Series A"], "sectors": ["Enterprise", "Consumer"], "check_size": "$500K-$5M", "aum": "$500M"},
    {"name": "Unusual Ventures", "location": "Menlo Park, CA", "stages": ["Seed", "Series A"], "sectors": ["Enterprise", "AI"], "check_size": "$1M-$20M", "aum": "$500M"},
    {"name": "Wing Venture Capital", "location": "Palo Alto, CA", "stages": ["Seed", "Series A"], "sectors": ["Enterprise", "AI", "Cybersecurity"], "check_size": "$500K-$10M", "aum": "$600M"},
    {"name": "Ridge Ventures", "location": "San Francisco, CA", "stages": ["Seed", "Series A"], "sectors": ["Enterprise", "AI"], "check_size": "$500K-$5M", "aum": "$300M"},
    {"name": "Notation Capital", "location": "Brooklyn, NY", "stages": ["Pre-Seed", "Seed"], "sectors": ["Enterprise", "Consumer"], "check_size": "$250K-$1M", "aum": "$100M"},
    {"name": "Betaworks", "location": "New York, NY", "stages": ["Pre-Seed", "Seed"], "sectors": ["Consumer", "AI"], "check_size": "$100K-$1M", "aum": "$150M"},
    {"name": "High Alpha", "location": "Indianapolis, IN", "stages": ["Seed", "Series A"], "sectors": ["Enterprise", "SaaS"], "check_size": "$500K-$10M", "aum": "$300M"},
    {"name": "Next Frontier Capital", "location": "Bozeman, MT", "stages": ["Seed", "Series A"], "sectors": ["Enterprise", "Consumer"], "check_size": "$500K-$3M", "aum": "$100M"},
    {"name": "Lead Edge Capital", "location": "New York, NY", "stages": ["Series B", "Growth"], "sectors": ["Enterprise", "SaaS"], "check_size": "$10M-$100M", "aum": "$2B"},
    {"name": "CRV", "location": "Menlo Park, CA", "stages": ["Seed", "Series A", "Series B"], "sectors": ["Enterprise", "Consumer", "AI", "Fintech"], "check_size": "$1M-$25M", "aum": "$4B"},
    {"name": "Spark Capital", "location": "San Francisco, CA", "stages": ["Seed", "Series A", "Series B"], "sectors": ["Consumer", "Enterprise"], "check_size": "$1M-$25M", "aum": "$3B"},
    {"name": "Social Capital", "location": "Palo Alto, CA", "stages": ["Seed", "Series A", "Series B"], "sectors": ["Healthcare", "Enterprise", "Consumer"], "check_size": "$1M-$25M", "aum": "$1.5B"},
    {"name": "SoftBank Vision Fund", "location": "San Carlos, CA", "stages": ["Series B", "Growth"], "sectors": ["Enterprise", "Consumer", "AI"], "check_size": "$50M-$500M", "aum": "$100B"},
    {"name": "Tiger Global Management", "location": "New York, NY", "stages": ["Seed", "Series A", "Series B", "Growth"], "sectors": ["Enterprise", "Consumer", "Fintech"], "check_size": "$1M-$500M", "aum": "$80B"},
    {"name": "Addition", "location": "New York, NY", "stages": ["Series A", "Series B", "Growth"], "sectors": ["Enterprise", "Consumer"], "check_size": "$5M-$100M", "aum": "$3B"},
    {"name": "Dragoneer Investment Group", "location": "San Francisco, CA", "stages": ["Series B", "Growth"], "sectors": ["Enterprise", "Consumer"], "check_size": "$25M-$200M", "aum": "$25B"},
    {"name": "D1 Capital Partners", "location": "New York, NY", "stages": ["Series B", "Growth"], "sectors": ["Enterprise", "Consumer"], "check_size": "$25M-$100M", "aum": "$20B"},
    {"name": "General Atlantic", "location": "New York, NY", "stages": ["Growth"], "sectors": ["Enterprise", "Consumer", "Healthcare", "Fintech"], "check_size": "$50M-$500M", "aum": "$90B"},
    {"name": "TA Associates", "location": "Boston, MA", "stages": ["Growth"], "sectors": ["Enterprise", "Healthcare", "Fintech"], "check_size": "$50M-$500M", "aum": "$50B"},
    {"name": "Summit Partners", "location": "Boston, MA", "stages": ["Growth"], "sectors": ["Enterprise", "Healthcare"], "check_size": "$50M-$500M", "aum": "$40B"},
    {"name": "TCV", "location": "Menlo Park, CA", "stages": ["Growth"], "sectors": ["Enterprise", "Consumer"], "check_size": "$50M-$500M", "aum": "$15B"},
    {"name": "Correlation Ventures", "location": "San Diego, CA", "stages": ["Seed", "Series A", "Series B"], "sectors": ["Enterprise", "Healthcare", "AI"], "check_size": "$100K-$10M", "aum": "$350M"},
    {"name": "Heroic Ventures", "location": "San Francisco, CA", "stages": ["Pre-Seed", "Seed"], "sectors": ["Enterprise", "Defense", "AI"], "check_size": "$500K-$5M", "aum": "$150M"},
    {"name": "Golden Ventures", "location": "Toronto, Canada", "stages": ["Pre-Seed", "Seed"], "sectors": ["Enterprise", "Consumer"], "check_size": "$250K-$1.5M", "aum": "$150M"},
    {"name": "Point Nine Capital", "location": "Berlin, Germany", "stages": ["Seed", "Series A"], "sectors": ["SaaS", "Enterprise", "Marketplaces"], "check_size": "$500K-$5M", "aum": "$500M"},
    {"name": "3Lines Venture Capital", "location": "Palo Alto, CA", "stages": ["Seed", "Series A"], "sectors": ["AI", "Enterprise", "Fintech"], "check_size": "$1M-$5M", "aum": "$100M"},
    {"name": "1843 Capital", "location": "Boston, MA", "stages": ["Series A", "Series B"], "sectors": ["Healthcare", "Fintech", "Cybersecurity"], "check_size": "$2M-$15M", "aum": "$150M"},
    {"name": "12/12 Ventures", "location": "Denver, CO", "stages": ["Seed", "Series A"], "sectors": ["Cannabis"], "check_size": "$500K-$5M", "aum": "$100M"},
    {"name": "Lowercase Capital", "location": "San Francisco, CA", "stages": ["Pre-Seed", "Seed"], "sectors": ["Consumer", "Enterprise"], "check_size": "$25K-$500K", "aum": "$300M"},
    {"name": "SV Angel", "location": "San Francisco, CA", "stages": ["Pre-Seed", "Seed"], "sectors": ["Consumer", "Enterprise", "AI"], "check_size": "$100K-$1M", "aum": "$500M"},
    {"name": "Structure Capital", "location": "San Francisco, CA", "stages": ["Pre-Seed", "Seed"], "sectors": ["Fintech", "AI", "Enterprise"], "check_size": "$100K-$500K", "aum": "$50M"},
    {"name": "True Ventures", "location": "San Francisco, CA", "stages": ["Seed", "Series A"], "sectors": ["Consumer", "Enterprise"], "check_size": "$1M-$15M", "aum": "$3B"},
    {"name": "Obvious Ventures", "location": "San Francisco, CA", "stages": ["Seed", "Series A", "Series B"], "sectors": ["Climate", "Healthcare", "Consumer"], "check_size": "$1M-$15M", "aum": "$700M"},
    {"name": "Data Collective DCVC", "location": "Palo Alto, CA", "stages": ["Seed", "Series A", "Series B"], "sectors": ["Deeptech", "AI", "Climate", "Healthcare"], "check_size": "$1M-$25M", "aum": "$3B"},
    {"name": "Congruent Ventures", "location": "San Francisco, CA", "stages": ["Seed", "Series A"], "sectors": ["Climate", "Sustainability"], "check_size": "$500K-$5M", "aum": "$400M"},
    {"name": "Footwork", "location": "San Francisco, CA", "stages": ["Seed", "Series A"], "sectors": ["Enterprise", "Consumer"], "check_size": "$1M-$10M", "aum": "$200M"},
    {"name": "Freestyle Capital", "location": "San Francisco, CA", "stages": ["Seed", "Series A"], "sectors": ["Enterprise", "Consumer"], "check_size": "$500K-$3M", "aum": "$400M"},
    {"name": "Menlo Ventures", "location": "Menlo Park, CA", "stages": ["Seed", "Series A", "Series B", "Growth"], "sectors": ["Enterprise", "Consumer", "Healthcare"], "check_size": "$1M-$100M", "aum": "$6B"},
    {"name": "NEA", "location": "Menlo Park, CA", "stages": ["Seed", "Series A", "Series B", "Growth"], "sectors": ["Enterprise", "Healthcare", "Consumer"], "check_size": "$1M-$100M", "aum": "$25B"},
    {"name": "Thrive Capital", "location": "New York, NY", "stages": ["Seed", "Series A", "Series B", "Growth"], "sectors": ["Consumer", "Enterprise", "Fintech"], "check_size": "$1M-$100M", "aum": "$15B"},
    {"name": "Ribbit Capital", "location": "Palo Alto, CA", "stages": ["Seed", "Series A", "Series B"], "sectors": ["Fintech"], "check_size": "$1M-$50M", "aum": "$5B"},
    {"name": "QED Investors", "location": "Alexandria, VA", "stages": ["Seed", "Series A", "Series B"], "sectors": ["Fintech"], "check_size": "$1M-$30M", "aum": "$3B"},
    {"name": "Fintech Collective", "location": "New York, NY", "stages": ["Seed", "Series A"], "sectors": ["Fintech"], "check_size": "$500K-$5M", "aum": "$500M"},
    {"name": "Nyca Partners", "location": "New York, NY", "stages": ["Seed", "Series A", "Series B"], "sectors": ["Fintech"], "check_size": "$5M-$30M", "aum": "$1.5B"},
    {"name": "FinVC", "location": "San Francisco, CA", "stages": ["Seed", "Series A"], "sectors": ["Fintech"], "check_size": "$500K-$3M", "aum": "$100M"},
]

# Add region based on location
def get_region(location):
    if 'Israel' in location:
        return 'Israel'
    elif 'Canada' in location:
        return 'USA'
    elif 'Germany' in location or 'UK' in location or 'London' in location:
        return 'Europe'
    else:
        return 'USA'

# Merge new VCs
all_vcs = list(existing_vcs)
added_count = 0
skipped = []

for vc_list in [NEW_ISRAELI_VCS, NEW_US_VCS]:
    for vc in vc_list:
        name_lower = vc['name'].lower()
        if name_lower not in existing_names:
            vc['region'] = get_region(vc['location'])
            if 'aum' not in vc:
                vc['aum'] = ''
            all_vcs.append(vc)
            existing_names.add(name_lower)
            added_count += 1
            print(f"Added: {vc['name']} ({vc['region']})")
        else:
            skipped.append(vc['name'])

print(f"\n{'='*50}")
print(f"Added: {added_count} new VCs")
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
