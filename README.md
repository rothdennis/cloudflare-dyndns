# Cloudflare DynDNS

## Setup

### Create a Cloudflare API Token

1. Create new API token [here](https://dash.cloudflare.com/profile/api-tokens)
2. Click `Create Token`
3. Click on `Use template` for `Edit zone DNS`
4. Under `Zone Resources` select your domain
5. Click `Continue to summary`
6. Click `Create Token`

### Get the Zone ID

1. Go to your [dashboard](https://dash.cloudflare.com/)
2. Select your domain
3. Scroll down to the `API` section
4. Copy the `Zone ID`


### Start the container

Example `compose.yml`:

```yml
services:
  cloudflare-dyndns:
    image: ghcr.io/rothdennis/cloudflare-dyndns
    container_name: cloudflare-dyndns
    restart: unless-stopped
    environment:
      ZONE_ID : << ZONE ID >>
      API_TOKEN : << API TOKEN >>
      SUBDOMAIN : << SUBDOMAIN >>
      REFRESH_INTERVAL: 1800        # Optional, default: 300
      IPV6 : True                   # Optional, default: False
      PROXIED : True                # Optional, default: False
```