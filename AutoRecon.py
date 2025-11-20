import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python autorecon.py <domain>")
        return
    
    domain = sys.argv[1]
    print(f"[+] Target: {domain}")

if __name__ == "__main__":
    main()
