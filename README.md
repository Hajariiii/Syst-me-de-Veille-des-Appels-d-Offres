
# Système de veille des appels d'offres

## Description


L'application réalise l'extraction des différents données des appels d'offres publiés sur le website : MarchesPublics.gov.ma, et le filtrage de ces offres selons les filtres choisi par l'utilisateur.
L'output est un tableau de données composés de 10 colonnes:
- Catégorie
- Procédure
- Référence
- Consultation ( lien de la page consultation de l'appel d'offre )
- Lieu d'exécution
- Objet
- Acheteur MarchesPublics
- Date limite de remise des plis
- Heure limits
- Date de publication





## Requirements

- Télécharger le chrome driver approprié pour votre appareil à partir du lien :
https://chromedriver.chromium.org/downloads
- Installer les packages de requirements.txt

## Utilisation

1. Saisir les paramètres appropriés à savoir :
![1ère page](https://github.com/Hajariiii/Syst-me-de-Veille-des-Appels-d-Offres/blob/main/1erePage.png?raw=true)
- Le chemin vers le Chrome Driver.
- Les filtres, par exemple : " étude Digitalisation " en séparant les termes par des espaces, des virgules, des points, 'et', 'ou'..
et valider en cliquant sur "Valider les paramètres".

2. Lancer l’opération :
![2ème page](https://github.com/Hajariiii/Syst-me-de-Veille-des-Appels-d-Offres/blob/main/2emePage.png?raw=true)
- Sur la deuxième page, vérifiez le chemin et les filtres, puis cliquez sur : "Commencer l'extraction".
- Vous allez remarquer l'ouverture d'une fenêtre Chrome qui est contrôlée par le driver : l'extraction va y avoir lieu. Vous pouvez réduire cette fenêtre sans souci.
- Le système peut prendre entre 10 à 15 mins pour compléter l'exécution. 
- La fin de l'extraction sera marquée par la fermeture de la fenêtre contrôlée et par le téléchargement réussi de votre dataset.

3. Collecter le tableau "Appels d'offre jj/mm/yyyy.xlsx"


## Finalement :
[Ce projet vient dans le cadre de mon stage de formation au sein de l'OCP Solutions.]

Encadré par : 
KRIMOU Kawtar , Project Manager chez OCP Solutions.

Et réalisé par :
BELRHITI Hajar, élève ingénieure arts et métiers en 5ème année, filière : intelligence artificielle et data science.
