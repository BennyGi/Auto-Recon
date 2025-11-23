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

    # ---------- WHOIS ----------
    print("[+] Running WHOIS...")
    whois_output = run_cmd(f"whois {domain}")

    with open(f"{outdir}/whois.txt", "w") as f:
        f.write(whois_output)

    print("[+] WHOIS saved to results/" + domain + "/whois.txt")
    

    # ---------- DIG / DNS ----------
    print("[+] Running DIG...")
    dns_output = run_cmd(f"dig {domain} ANY +noidnout")

    with open(f"{outdir}/dns.txt", "w") as f:
        f.write(dns_output)

    print("[+] DNS saved to results/" + domain + "/dns.txt")


    # ---------- NMAP ----------
    print("[+] Running NMAP...")
    nmap_output = run_cmd(f"nmap -sV --min-rate 500 {domain}")

    with open(f"{outdir}/nmap.txt", "w") as f:
        f.write(nmap_output)

    print("[+] NMAP saved to results/" + domain + "/nmap.txt")


    # ---------- FFUF ----------
    print("[+] Running FFUF...")

    wordlist = "/usr/share/wordlists/dirb/common.txt"
    ffuf_cmd = f"ffuf -u http://{domain}/FUZZ -w {wordlist} -mc 200,301,302 -t 40"
    ffuf_output = run_cmd(ffuf_cmd)
    
    with open(f"{outdir}/ffuf.txt", "w") as f:
        f.write(ffuf_output)

    print("[+] FFUF saved to results/" + domain + "/ffuf.txt")

if __name__ == "__main__":
    main()
