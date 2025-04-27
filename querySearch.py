import requests
from googlesearch import search
from bs4 import BeautifulSoup
import json
import time
import re

# Charger les données des entreprises
with open('company_results.json', 'r') as file:
    data = json.load(file)

def is_valid_website(url):
    """Vérifie si l'URL est un site web valide."""
    if not url:
        return False
        
    # Liste des domaines à exclure
    excluded_domains = [
        'data.gouv.fr',
        'google.com',
        'google.fr',
        'search?',
        'tel:',
        'mailto:'
    ]
    
    # Vérifier si l'URL contient un domaine exclu
    for domain in excluded_domains:
        if domain in url:
            return False
            
    # Vérifier si l'URL commence par http ou https
    if not url.startswith(('http://', 'https://')):
        return False
        
    return True

def is_valid_name(name):
    """Vérifie si le nom de l'entreprise est valide."""
    if not name or name == "None" or name == "[ND]" or name == "null":
        return False
    return True

def find_website_from_name(name):
    """Recherche le site web d'une entreprise à partir de son nom."""
    if not is_valid_name(name):
        return None
        
    query = f"{name} site officiel"
    try:
        # The search function doesn't support 'num' parameter, so we'll use a list comprehension
        # to get the first 5 results
        results = list(search(query, lang="fr"))[:5]
        if results:
            # Filtrer les URLs invalides
            valid_urls = [url for url in results if is_valid_website(url)]
            return valid_urls[0] if valid_urls else None
        return None
    except Exception as e:
        print(f"Error searching for {name}: {e}")
        return None

if __name__ == "__main__":
    # Dictionnaire pour stocker les résultats
    website_results = {}
    
    # Traiter chaque entreprise
    total_companies = len(data)
    valid_companies = 0
    
    for i, (siren, company_data) in enumerate(data.items(), 1):
        name = company_data["name"]
        
        # Vérifier si le nom est valide
        if not is_valid_name(name):
            print(f"\nSkipping {i}/{total_companies}: Nom invalide ({name})")
            continue
            
        print(f"\nTraitement {i}/{total_companies}: {name}")
        
        # Rechercher le site web
        site = find_website_from_name(name)
        
        # Ne sauvegarder que si un site web a été trouvé
        if site:
            website_results[siren] = {
                "name": name,
                "website": site
            }
            valid_companies += 1
            print(f"Site web trouvé: {site}")
        else:
            print("Aucun site web trouvé")
        
        # Sauvegarder les résultats après chaque entreprise
        with open('website_results.json', 'w', encoding='utf-8') as f:
            json.dump(website_results, f, ensure_ascii=False, indent=2)
        
        # Pause pour ne pas surcharger Google
        time.sleep(0.2)
    
    print(f"\nTraitement terminé. {valid_companies} entreprises valides trouvées.")
    print("Résultats sauvegardés dans website_results.json")
