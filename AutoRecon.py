import sys
import subprocess
import os

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout

def main():
    if len(sys.argv) < 2:
        print("Usage: python autorecon.py <domain>")
        return
    
    domain = sys.argv[1]
    print(f"[+] Target: {domain}")

    outdir = f"results/{domain}"
    os.makedirs(outdir, exist_ok=True)

    # WHOIS 
    print("[+] Running WHOIS...")
    whois_output = run_cmd(f"whois {domain}")

    # Saving the file
    with open(f"{outdir}/whois.txt", "w") as f:
        f.write(whois_output)

    print("[+] WHOIS saved to results/" + domain + "/whois.txt")
    

    # DNS/DIG
    print("[+] Running DIG...")
    dns_output = run_cmd(f"dig{domain} ANY+noidnout")

      # Saving the file
    with open(f"{outdir}/dns.txt, "w") as f:
        f.write(dns_output)
    print("[+] DNS saved to results.")


    # NMAP
    print("[+] Running NMAP...")
    nmap_output = run_cmd(f"nmap -sV --min-rate 500 {domain}")

    
    # Saving the file
    with open(f"{outdir}/nmap.txt", "w") as f:
        f.write(nmap_output)

    print("[+] NMAP saved to results/" + domain + "/nmap.txt")


if __name__ == "__main__":
    main()
