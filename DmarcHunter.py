import dns.resolver
import subprocess

def check_mx(domain):
    try:
        answers = dns.resolver.resolve(domain, 'MX')
        mx_records = [str(r.exchange)[:-1] for r in answers]
        return mx_records
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
        return None
    except dns.exception.DNSException as e:
        print(f"Error while resolving MX for {domain}: {e}")
        return None

def check_dmarc(domain):
    try:
        result = subprocess.run(['dig', '+short', 'TXT', f'_dmarc.{domain}'], capture_output=True, text=True)
        dmarc_record = result.stdout.strip()
        return dmarc_record
    except subprocess.CalledProcessError:
        return None
    
def display_banner():
    banner_text = r"""
╔╦╗╔╦╗╔═╗╦═╗╔═╗  ╦ ╦╦ ╦╔╗╔╔╦╗╔═╗╦═╗
 ║║║║║╠═╣╠╦╝║    ╠═╣║ ║║║║ ║ ║╣ ╠╦╝
═╩╝╩ ╩╩ ╩╩╚═╚═╝  ╩ ╩╚═╝╝╚╝ ╩ ╚═╝╩╚═
"""
    print(banner_text)

def main():
    display_banner()

    # Define as sequências de escape ANSI para a cor vermelha, verde e a cor padrão
    red_color = "\033[91m"
    green_color = "\033[92m"
    reset_color = "\033[0m"

    file_path = 'domains.txt'  # Caminho para o arquivo contendo a lista de domínios

    with open(file_path, 'r') as file:
        domains = file.read().splitlines()

    for domain in domains:
        print(f"{green_color}Domain: {domain}{reset_color}")

        mx_records = check_mx(domain)
        if mx_records:
            print("MX Records:")
            for mx in mx_records:
                print(f"  {mx}")
        else:
            print("No MX records found.")

        dmarc_record = check_dmarc(domain)
        if dmarc_record:
            print("DMARC Record:")
            print(f"  {dmarc_record}")
            if "p=none" in dmarc_record:
                print(f"{red_color}DMARC existe, mas não há políticas para o mesmo{reset_color}")
            elif "p=quarantine" in dmarc_record:
                print(f"{red_color}A atual política de DMARC para este domínio é QUARANTINE{reset_color}")
            elif "p=reject" in dmarc_record:
                print(f"{red_color}A atual política de DMARC para este domínio é REJECT{reset_color}")
        else:
            print(f"{red_color}Registro DMARC não localizado para este domínio{reset_color}")

        print("=" * 50)

if __name__ == "__main__":
    main()
