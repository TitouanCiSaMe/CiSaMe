import os


def fusion_fichiers_texte_dossier(dossier, fichier_sortie, extension=".txt", separateur=""):
    """
    Fusionne tous les fichiers texte d'un dossier en un seul fichier.

    Args:
        dossier (str): Chemin vers le dossier contenant les fichiers à fusionner
        fichier_sortie (str): Chemin vers le fichier de sortie
        extension (str): Extension des fichiers à fusionner (.txt par défaut)
        separateur (str): Texte à insérer entre le contenu de chaque fichier
    """
    try:
        # Obtenir la liste des fichiers dans le dossier avec l'extension spécifiée
        fichiers = [f for f in os.listdir(dossier) if f.endswith(extension)]

        if not fichiers:
            print(f"Aucun fichier avec l'extension {extension} trouvé dans le dossier {dossier}")
            return

        # Trier les fichiers par nom (optionnel, mais souvent utile)
        fichiers.sort()

        # Créer le chemin complet vers le fichier de sortie
        chemin_sortie = os.path.join(dossier, fichier_sortie) if not os.path.isabs(fichier_sortie) else fichier_sortie

        with open(chemin_sortie, 'w', encoding='utf-8') as destination:
            for i, fichier in enumerate(fichiers):
                chemin_fichier = os.path.join(dossier, fichier)
                try:
                    with open(chemin_fichier, 'r', encoding='utf-8') as source:
                        print(f"Fusion du fichier: {fichier}")
                        contenu = source.read()
                        destination.write(contenu)

                        # Ajouter le séparateur sauf pour le dernier fichier
                        if i < len(fichiers) - 1:
                            destination.write(separateur)

                except Exception as e:
                    print(f"Erreur lors de la lecture du fichier {fichier}: {str(e)}")

        print(f"Fusion réussie! {len(fichiers)} fichiers ont été fusionnés dans {chemin_sortie}")

    except Exception as e:
        print(f"Erreur lors de la fusion: {str(e)}")


# Exemple d'utilisation
if __name__ == "__main__":
    # Spécifier le dossier contenant les fichiers
    dossier = "/home/titouan/Documents/Github/data/Articles"

    # Nom du fichier de sortie
    fichier_sortie = "/home/titouan/Documents/Github/data/Articles/Articles.txt"

    # Fusionner tous les fichiers .txt du dossier avec un double saut de ligne entre chaque fichier
    fusion_fichiers_texte_dossier(dossier, fichier_sortie, extension=".txt", separateur="\n\n"
