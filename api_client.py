import requests
import argparse

BASE = "http://localhost:5000"
API_KEY = {"X-API-KEY": "NotUs@2025!$"}

def list_contacts():
    r = requests.get(f"{BASE}/contacts")
    print(r.json())

def add_contact(name, phone):
    r = requests.post(f"{BASE}/contacts", json={"name": name, "phone": phone}, headers=API-KEY)
    print(r.status_code, r.json())

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("action", choices=["list", "add"])
    p.add_argument("--name")
    p.add_argument("--phone")
    args = p.parse_args()
    if args.action == "list":
        list_contacts()
    elif args.action == "add":
        add_contact(args.name, args.phone)
