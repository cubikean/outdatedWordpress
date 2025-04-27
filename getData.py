import requests
import json
import time
import os

# Charger la liste des SIREN
with open('siren_only.json', 'r') as file:
    siren_list = json.load(file)

# Configuration des headers
headers = {
    "accept": "application/json",
    "X-INSEE-Api-Key-Integration": "a079a52d-e516-4e11-b9a5-2de516fe116c"
}

# Dictionnaire pour stocker les résultats
results = {}

# Vérifier si le fichier company_results.json existe et le charger
if os.path.exists('company_results.json'):
    with open('company_results.json', 'r', encoding='utf-8') as f:
        results = json.load(f)
    print(f"Chargement des {len(results)} résultats existants...")

# Trouver l'index du dernier SIREN traité
last_siren = "803082593"
if last_siren:
    try:
        start_index = siren_list.index(last_siren)
        print(f"Reprise à partir du SIREN {last_siren} (index {start_index})")
    except ValueError:
        print(f"Le SIREN {last_siren} n'a pas été trouvé dans la liste. Démarrage depuis le début.")
        start_index = 0
else:
    start_index = 0

# Traiter les SIREN avec un délai d'une seconde entre chaque requête
for siren in siren_list[start_index:]:
    # Vérifier si le SIREN a déjà été traité
    if siren in results:
        print(f"SIREN {siren} déjà traité, passage au suivant...")
        continue
        
    url = f"https://api.insee.fr/api-sirene/3.11/siren/{siren}"
    
    try:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()  # Vérifier si la requête a réussi
        
        # Extraire les données de l'entreprise
        company_data = resp.json()["uniteLegale"]
        company_name = company_data["periodesUniteLegale"][0]["denominationUniteLegale"]
        
        # Stocker les résultats
        results[siren] = {
            "name": company_name,
            # "data": company_data
        }
        
        print(f"SIREN: {siren} - Nom: {company_name}")
        
    except Exception as e:
        print(f"Erreur pour le SIREN {siren}: {str(e)}")
        results[siren] = {
            "error": str(e)
        }
    
    # Attendre une seconde avant la prochaine requête
    time.sleep(2)
    
    # Sauvegarder les résultats après chaque requête
    with open('company_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

print("\nTraitement terminé. Résultats sauvegardés dans company_results.json")