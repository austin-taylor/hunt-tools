import requests
import pandas as pd

#Address for AT&T Modem
pull_macs_url = 'http://192.168.1.254/cgi-bin/home.ha'

#Load data into dataframe
df = pd.read_html(pull_macs_url, attrs={'width':'800'}, header=0)[0]

mac_addresses = df['MAC Address']

def vendor_loookup(mac):
    from urllib.parse import quote_plus
    vendor = None
    try:
        vendor_lookup = 'http://api.macvendors.com/%s' % quote_plus(mac)
        vendor_response = requests.get(vendor_lookup)
        if vendor_response.status_code != 200:
            vendor = 'No Vendor Found'
        else:
            vendor = vendor_response.text
    except:
        vendor = 'Error'
    return vendor
    
df['Vendor'] = mac_addresses.apply(vendor_loookup)

Vendor_DF = pd.DataFrame(df.groupby(['Vendor', 'Device IPv4 Address / Name', 'MAC Address']).size())
Vendor_DF = Vendor_DF.drop(0, axis=1)

Vendor_DF
