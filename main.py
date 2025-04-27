import subprocess
import time
import os
import sys

def run_script(script_name):
    """Exécute un script Python et affiche sa sortie en temps réel."""
    print(f"\n{'='*50}")
    print(f"Exécution de {script_name}")
    print(f"{'='*50}\n")
    
    try:
        # Exécuter le script directement avec python
        process = subprocess.Popen([sys.executable, script_name], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.STDOUT,
                                 universal_newlines=True,
                                 bufsize=1)  # Line buffered
        
        # Afficher la sortie en temps réel
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
                sys.stdout.flush()  # Forcer l'affichage immédiat
            
        # Attendre la fin du script
        return_code = process.wait()
        
        if return_code == 0:
            print(f"\n{script_name} s'est terminé avec succès.")
            return True
        else:
            print(f"\nErreur lors de l'exécution de {script_name} (code de retour: {return_code}).")
            return False
            
    except Exception as e:
        print(f"\nErreur lors de l'exécution de {script_name}: {str(e)}")
        return False

def main():
    print("Démarrage du pipeline de traitement...")
    
    # Vérifier que les fichiers nécessaires existent
    required_files = ['company_results.json']
    for file in required_files:
        if not os.path.exists(file):
            print(f"Erreur: Le fichier {file} n'existe pas.")
            return
    
    # Exécuter querySearch.py
    if not run_script('querySearch.py'):
        print("Arrêt du pipeline suite à une erreur dans querySearch.py")
        return
    
    # Attendre un peu entre les scripts
    time.sleep(2)
    
    # Exécuter checkWordpressVersion.py
    if not run_script('checkWordpressVersion.py'):
        print("Arrêt du pipeline suite à une erreur dans checkWordpressVersion.py")
        return
    
    print("\nPipeline de traitement terminé avec succès!")

if __name__ == "__main__":
    main() 