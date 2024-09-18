import pynetbox
import urllib3
import os
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# set env vars before executing the script
netbox_url = os.environ.get('NBURL',"")
api_token  = os.environ.get('NBAPI',"")
vrf_name   = os.environ.get('NBVRF',"") # the name of the VRF in string
if not (netbox_url and api_token and vrf_name):
    raise Exception("missing NBURL/NBAPINBVRF env vars")
nb = pynetbox.api(netbox_url, token=api_token)
nb.http_session.verify = False
f = open("hosts.netbox", "w")
vrf = nb.ipam.vrfs.get(name=vrf_name)
if vrf:
    # Get all IP addresses in the VRF with a DNS name
    ip_addresses = nb.ipam.ip_addresses.filter(vrf_id=vrf.id, dns_name__empty=False)
    print(f"collected {len(ip_addresses)} ip/names from netbox")
    for ip in ip_addresses:
        f.write(f"{ip.address.split('/')[0]} {ip.dns_name}\n")
else:
    print(f"FAIL: VRF '{vrf_name}' not found")
    f.close()
    sys.exit(1)
f.close()
