import dns.resolver
from rich import print

"""
requirements:
    pip install dnspython rich
    
characters:
    https://www.w3.org/TR/xml-entity-names/025.html
    ╼
    ┏
    ►
    ┡
"""

hosts = ["facebook.com", "google.pl", "microsoft.com", "youtube.com", "github.com", "wikipedia.org"]
# color = 'red'
color = 'cyan'
for index, host in enumerate(hosts, start=1):
    print(f'{index}.[{color}]┏ [/{color}]{host}')
    ips = dns.resolver.resolve(host, "A")
    ips_number = len(ips)
    pattern = f'[{color}]  ┡╼► [/{color}]'
    for i, ip in enumerate(ips, start=1):
        if i == ips_number:
            pattern = f'[{color}]  ┗╼► [/{color}]'
        print(f'{pattern}{ip}')
    print()
    