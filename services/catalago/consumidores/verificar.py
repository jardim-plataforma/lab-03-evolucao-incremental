import argparse
import json
from urllib.request import urlopen
from consumidores.portal import interpretar as portal
from consumidores.integracao import interpretar as integracao

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:8080")
    args = parser.parse_args()
    with urlopen(args.base_url.rstrip("/") + "/api/v1/recursos/svc-001", timeout=5) as response:
        payload = json.load(response)
    print("Portal:", portal(payload))
    print("Integração:", integracao(payload))

if __name__ == "__main__":
    main()
