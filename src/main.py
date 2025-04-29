import requests
import os
import re
from dotenv import load_dotenv
import logging
import sys
from cloudflare import Cloudflare
import time

# Load environment variables from .env file
load_dotenv()

# Set up custom logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    fmt='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
handler.setFormatter(formatter)
logger.addHandler(handler)

# Load environment variables
ZONE_ID = os.environ.get('ZONE_ID')
API_TOKEN = os.environ.get('API_TOKEN')
SUBDOMAIN = os.environ.get('SUBDOMAIN')
REFESH_INTERVAL = int(os.environ.get('REFRESH_INTERVAL', 300))
IPV6 = os.environ.get('IPV6', 'false').lower() in ['y', 'yes', 't', 'true', 'on', '1']
PROXIED = os.environ.get('PROXIED', 'False').lower() in ['y', 'yes', 't', 'true', 'on', '1']

def get_external_ip(ipv6):
    requests.packages.urllib3.util.connection.HAS_IPV6 = ipv6
    response = requests.get('https://cloudflare.com/cdn-cgi/trace')
    ip = re.findall(r'ip=(.*)', response.text)[0]
    return ip

def get_zone_details(zone_id, api_token):
    client = Cloudflare(api_token=api_token)
    response = client.zones.get(
        zone_id=zone_id
    )
    return response

def get_dns_records(zone_id, api_token):
    client = Cloudflare(api_token=api_token)
    response = client.dns.records.list(
        zone_id=zone_id
    )
    return response

def create_dns_record(api_token, zone_id, ip, subdomain, proxied, use_ipv6):
    client = Cloudflare(api_token=api_token)
    response = client.dns.records.create(
        zone_id=zone_id,
        content=ip,
        name=subdomain,
        proxied=proxied,
        type='AAAA' if use_ipv6 else 'A'
    )
    return response

def update_dns_record(api_token, zone_id, dns_record_id, ip, subdomain, proxied, use_ipv6):
    client = Cloudflare(api_token=api_token)
    response = client.dns.records.update(
        zone_id=zone_id,
        dns_record_id=dns_record_id,
        content=ip,
        name=subdomain,
        proxied=proxied,
        type='AAAA' if use_ipv6 else 'A'
    )
    return response

if __name__ == "__main__":

    # check setup
    if not ZONE_ID:
        logger.error('ZONE_ID is not set.')
        sys.exit(1)

    if not API_TOKEN:
        logger.error('API_TOKEN is not set.')
        sys.exit(1)

    if not SUBDOMAIN:
        logger.error('SUBDOMAIN is not set.')
        sys.exit(1)

    current_ip = ''

    while True:

        if current_ip != '':
            time.sleep(REFESH_INTERVAL)

        # Fetch the external IP address
        try:
            logger.info('Fetching the external IP address...')
            current_ip = get_external_ip(IPV6)
            logger.info(f'The external IP address is: {current_ip}')
        except Exception as e:
            logger.error(f'Error fetching external IP address: {e}')
            continue

        # Fetch the zone details -> domain name
        try:
            logger.info('Fetching zone details...')
            zone_details = get_zone_details(ZONE_ID, API_TOKEN)
            logger.info(f'Zone details fetched successfully for {zone_details.name}')
        except Exception as e:
            logger.error(f'Error fetching zone details: {e}')
            continue

        # Fetch the DNS records
        try:
            logger.info('Fetching DNS records...')
            dns_records = get_dns_records(ZONE_ID, API_TOKEN)
            logger.info('DNS records fetched successfully.')
        except Exception as e:
            logger.error(f'Error fetching DNS records: {e}')
            continue

        # Check if the DNS record already exists
        for dns_record in dns_records:
            if dns_record.name == f'{SUBDOMAIN}.{zone_details.name}':
                # ip has not changed -> no update needed
                if current_ip == dns_record.content and dns_record.proxied == PROXIED and dns_record.type == ('AAAA' if IPV6 else 'A'):
                    logger.info(f'Values have not changed for {SUBDOMAIN}.{zone_details.name}. No update needed.')
                # ip has changed -> update DNS record
                else:
                    try:
                        logger.info('Updating existing DNS record...')
                        update_dns_record(API_TOKEN, ZONE_ID, dns_record.id, current_ip, SUBDOMAIN, PROXIED, IPV6)
                        logger.info(f'DNS record updated successfully for {SUBDOMAIN}.{zone_details.name} to IP {current_ip}')
                    except Exception as e:
                        logger.error(f'Error updating DNS record: {e}')
                break
        else:
            # If the DNS record does not exist, create it
            try:
                logger.info('Creating new DNS record...')
                create_dns_record(API_TOKEN, ZONE_ID, current_ip, SUBDOMAIN, PROXIED, IPV6)
                logger.info(f'DNS record created successfully for {SUBDOMAIN}.{zone_details.name} and IP {current_ip}')
            except Exception as e:
                logger.error(f'Error creating DNS record: {e}')
            