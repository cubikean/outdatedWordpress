import json

def extract_siren():
    # Lecture du fichier source
    try:
        with open('charente_maritime_siren.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            
        # Extraction des SIREN uniquement
        siren_list = []
        for item in data:
            if 'siren' in item:
                siren_list.append(item['siren'])
        
        # Écriture dans un nouveau fichier
        with open('siren_only.json', 'w', encoding='utf-8') as output:
            json.dump(siren_list, output, indent=2, ensure_ascii=False)
            
        print(f"Extraction terminée. {len(siren_list)} SIREN ont été extraits.")
        
    except FileNotFoundError:
        print("Le fichier charente_maritime_siren.json n'a pas été trouvé.")
    except json.JSONDecodeError:
        print("Erreur lors de la lecture du fichier JSON.")
    except Exception as e:
        print(f"Une erreur est survenue: {str(e)}")

if __name__ == "__main__":
    extract_siren()
