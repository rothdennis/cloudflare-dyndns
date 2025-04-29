# Docker Cloudflare DynDNS

This small Alpine Linux based Docker image will allow you to use the free Cloudflare DNS Service as a Dynamic DNS Provider (DynDNS).

Supported plattforms:

|Plattform|Architecture|
|---|---|
|Linux|amd64|

Supported registries:
- [GitHub Container Registry]()

## Usage

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
      REFRESH_INTERVAL: 1800
      IPV6 : True
      PROXIED : True
```

## Parameters
|Variable|Description|Optional|Type|
|---|---|---|---|
|ZONE_ID|Cloudflare Zone ID|No|String|
|API_TOKEN|Cloudflare API Token|No|String|
|SUBDOMAIN|Subdomain to update|No|String|
|REFRESH_INTERVAL|Interval to check for IP changes in seconds|Yes|Integer (default: 300)|
|IPV6|Use IPv6|Yes|Boolean (default: False)|
|PROXIED|Use Cloudflare proxy|Yes|Boolean (default: False)|

## Creating a Cloudflare API token

1. Create new API token [here](https://dash.cloudflare.com/profile/api-tokens)
2. Click `Create Token`
3. Click on `Use template` for `Edit zone DNS`
4. Under `Zone Resources` select your domain
5. Click `Continue to summary`
6. Click `Create Token`

## Getting the Cloudflare Zone ID

1. Go to your [dashboard](https://dash.cloudflare.com/)
2. Select your domain
3. Scroll down to the `API` section
4. Copy the `Zone ID`


