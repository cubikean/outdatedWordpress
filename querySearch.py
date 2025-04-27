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

def find_website_from_name(name, max_retries=3):
    """Recherche le site web d'une entreprise à partir de son nom."""
    if not is_valid_name(name):
        return None
        
    query = f"{name} site officiel"
    retry_count = 0
    base_delay = 2  # Délai de base de 2 secondes
    
    while retry_count < max_retries:
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
            if "429" in str(e):  # Erreur Too Many Requests
                retry_count += 1
                if retry_count < max_retries:
                    delay = base_delay * (2 ** retry_count)  # Délai exponentiel
                    print(f"Trop de requêtes, attente de {delay} secondes avant de réessayer...")
                    time.sleep(delay)
                    continue
            print(f"Error searching for {name}: {e}")
            return None

if __name__ == "__main__":
    # Dictionnaire pour stocker les résultats
    website_results = {}
    
    # Statistiques
    stats = {
        "total": len(data),
        "traitées": 0,
        "sites_trouvés": 0,
        "noms_invalides": 0,
        "données_invalides": 0,
        "erreurs": 0
    }
    
    # Traiter chaque entreprise
    for i, (siren, company_data) in enumerate(data.items(), 1):
        # Afficher le statut actuel
        print("\n" + "="*50)
        print(f"Progression: {i}/{stats['total']} ({(i/stats['total']*100):.1f}%)")
        print(f"Statut actuel:")
        print(f"- Sites trouvés: {stats['sites_trouvés']}")
        print(f"- Noms invalides: {stats['noms_invalides']}")
        print(f"- Données invalides: {stats['données_invalides']}")
        print(f"- Erreurs: {stats['erreurs']}")
        print("="*50)
        
        # Vérifier si les données de l'entreprise sont valides
        if not isinstance(company_data, dict):
            print(f"\nSkipping {i}/{stats['total']}: Données invalides")
            stats['données_invalides'] += 1
            continue
            
        # Récupérer le nom de l'entreprise
        name = company_data.get("name")
        
        # Vérifier si le nom est valide
        if not is_valid_name(name):
            print(f"\nSkipping {i}/{stats['total']}: Nom invalide ({name})")
            stats['noms_invalides'] += 1
            continue
            
        print(f"\nTraitement {i}/{stats['total']}: {name}")
        
        # Rechercher le site web
        site = find_website_from_name(name)
        
        # Ne sauvegarder que si un site web a été trouvé
        if site:
            website_results[siren] = {
                "name": name,
                "website": site
            }
            stats['sites_trouvés'] += 1
            print(f"Site web trouvé: {site}")
        else:
            stats['erreurs'] += 1
            print("Aucun site web trouvé")
        
        stats['traitées'] += 1
        
        # Sauvegarder les résultats après chaque entreprise
        with open('website_results.json', 'w', encoding='utf-8') as f:
            json.dump(website_results, f, ensure_ascii=False, indent=2)
        
        # Pause pour ne pas surcharger Google
        time.sleep(2)  # Augmentation du délai à 2 secondes
    
    # Afficher le résumé final
    print("\n" + "="*50)
    print("RÉSUMÉ FINAL")
    print("="*50)
    print(f"Total des entreprises: {stats['total']}")
    print(f"Entreprises traitées: {stats['traitées']}")
    print(f"Sites web trouvés: {stats['sites_trouvés']}")
    print(f"Noms invalides: {stats['noms_invalides']}")
    print(f"Données invalides: {stats['données_invalides']}")
    print(f"Erreurs: {stats['erreurs']}")
    print("="*50)
    print("Résultats sauvegardés dans website_results.json")
