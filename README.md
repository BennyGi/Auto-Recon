# Auto-Recon
A lightweight automated recon tool for pentesting practice.

## MVP
Input: domain (e.g., target.com)

Output:
- Basic WHOIS info
- DNS info (dns records)
- Nmap basic scan
- Directory scan (ffuf)
- Results saved under results/target/
- Final summary report (text/markdown)

## Technologies
- Python (subprocess)
- Linux tools: whois, dig, nmap, ffuf
