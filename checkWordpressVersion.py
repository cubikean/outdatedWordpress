import json
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

# Current WordPress version to check against
CURRENT_WP_VERSION = "6.8"

def check_wordpress_version(url):
    try:
        # Add /feed/ to URL
        feed_url = urljoin(url.rstrip('/'), '/feed/')
        
        # Make request with timeout
        response = requests.get(feed_url, timeout=10)
        
        if response.status_code == 200:
            # Look for WordPress version in feed
            wp_version_match = re.search(r'https://wordpress.org/\?v=([\d.]+)', response.text)
            if wp_version_match:
                return wp_version_match.group(1)
    except:
        pass
    return None

def find_emails(url):
    """Recherche les adresses email sur le site."""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            # Recherche des emails dans le texte de la page
            email_pattern = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}'
            emails = re.findall(email_pattern, response.text)
            
            # Filtrer les emails invalides et les doublons
            valid_emails = []
            for email in emails:
                # Vérifier que l'email n'est pas dans une URL ou un texte de lien
                if not re.search(r'<a[^>]*>' + re.escape(email), response.text):
                    valid_emails.append(email.lower())
            
            return list(set(valid_emails))  # Supprimer les doublons
    except:
        pass
    return []

# Load website data
with open('website_results.json') as f:
    websites = json.load(f)

# Store results
results = {}

# Check each website
for company_id, data in websites.items():
    website = data['website']
    wp_version = check_wordpress_version(website)
    
    if wp_version:
        emails = find_emails(website)
        results[company_id] = {
            'name': data['name'],
            'website': website,
            'wordpress_version': wp_version,
            'needs_update': wp_version < CURRENT_WP_VERSION,
            'emails': emails
        }

# Save results
with open('wordpress_versions.json', 'w') as f:
    json.dump(results, f, indent=2)
