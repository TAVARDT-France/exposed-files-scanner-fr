<p align="center">
  <a href="https://ag.tavardt.com/fr/">
    <img src="https://ag.tavardt.com/img/tavardt-banner.png" alt="TAVARDT" width="1024" />
  </a>
</p>

# Scanner de Fichiers et Identifiants Exposés

[![Scanner Fichiers Exposes](https://img.shields.io/badge/TAVARDT-Surface%20Attaque-5b3cf5.svg)](https://tools.tavardt.com/fr/scanner-fichiers-exposes/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Outil d'audit automatisé de surface d'attaque pour la détection de fichiers d'environnement exposés, sauvegardes de bases de données, métadonnées git et identifiants cloud.

Le moteur inspecte les périmètres web pour identifier les erreurs de configuration de serveurs et les fuites involontaires de données sensibles avant leur exploitation par des cyberattaquants. Développé sans dépendance externe, il s'exécute nativement en console Python et dans les chaînes d'intégration de sécurité.

***

## Périmètre de Détection de Surface et Architecture des Menaces

L'exposition involontaire de ressources confidentielles à la racine des serveurs web constitue l'un des vecteurs d'Accès Initial les plus dangereux dans l'écosystème numérique. Des serveurs Nginx, Apache, Caddy ou des compartiments S3 mal paramétrés diffusent régulièrement des fichiers masqués et des exports SQL à des clients non authentifiés.

* **Variables d'Environnement et Secrets**: Détection active des fichiers `.env`, `.env.local` et `.env.production` hébergeant des mots de passe de bases de données, des clés de chiffrement et des jetons d'API.
* **Métadonnées de Gestion de Version**: Analyse des répertoires `/.git/HEAD` et `/.git/config`, empêchant les attaquants de reconstruire la totalité du code source propriétaire.
* **Sauvegardes de Bases de Données**: Repérage d'exports SQL critiques tels que `backup.sql`, `dump.sql` et `database.sql`, contenant l'ensemble des tables et des données applicatives.
* **Infrastructure et Orchestration**: Contrôle des définitions de conteneurs dans `docker-compose.yml` et des données de diagnostic via `phpinfo.php` et `config.json`.
* **Identifiants d'Accès aux Fournisseurs Cloud**: Recherche des fichiers `/.aws/credentials`, prévenant la compromission administrative d'infrastructures cloud.
* **Conformité Normative**: Structuré en parfaite cohérence avec les Recommandations de Sécurité de l'ANSSI et RGPD (CNIL).

***

## Matrice d'Inspection de Surface d'Attaque

<table>
  <thead>
    <tr>
      <th align="left">Chemin Surveillé</th>
      <th align="left">Sévérité</th>
      <th align="left">Vecteur de Risque et Type d'Actif</th>
      <th align="left">Mesure de Durcissement Recommandée</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>/.env</code></td>
      <td>CRITIQUE</td>
      <td>Variables d'environnement, accès aux bases de données et clés privées d'API.</td>
      <td>Interdire l'accès aux fichiers préfixés d'un point ou les déplacer hors de la racine web.</td>
    </tr>
    <tr>
      <td><code>/.env.local</code></td>
      <td>CRITIQUE</td>
      <td>Paramètres de développement et secrets de test déployés par inadvertance en production.</td>
      <td>Configurer des règles .gitignore rigoureuses et rejeter les dotfiles sur le proxy inverse.</td>
    </tr>
    <tr>
      <td><code>/.env.production</code></td>
      <td>CRITIQUE</td>
      <td>Identifiants opérationnels des services de production et secrets de tiers.</td>
      <td>Remplacer les fichiers statiques par des gestionnaires de coffres-forts numériques.</td>
    </tr>
    <tr>
      <td><code>/.git/HEAD</code></td>
      <td>CRITIQUE</td>
      <td>Pointeur de branche git révélant la structure et les branches du dépôt de code.</td>
      <td>Bloquer le dossier /.git sur le serveur web et purger les dossiers git lors du déploiement.</td>
    </tr>
    <tr>
      <td><code>/.git/config</code></td>
      <td>CRITIQUE</td>
      <td>Adresses des dépôts distants, chemins internes et jetons d'accès éventuellement intégrés.</td>
      <td>Restreindre l'accès aux données de gestion de versions sur l'ensemble des hôtes virtuels.</td>
    </tr>
    <tr>
      <td><code>/backup.sql</code></td>
      <td>CRITIQUE</td>
      <td>Exportation complète de base de données contenant tables, empreintes et données d'utilisateurs.</td>
      <td>Conserver les sauvegardes uniquement dans un stockage cloud privé avec chiffrement au repos.</td>
    </tr>
    <tr>
      <td><code>/dump.sql</code></td>
      <td>CRITIQUE</td>
      <td>Sauvegarde brute laissée sur le serveur à la suite de manipulations techniques manuelles.</td>
      <td>Mettre en place des scripts de nettoyage automatique après chaque déploiement.</td>
    </tr>
    <tr>
      <td><code>/database.sql</code></td>
      <td>CRITIQUE</td>
      <td>Structure du schéma relationnel et données de démarrage de l'application.</td>
      <td>Proscrire la présence de scripts de base de données dans les répertoires publics du serveur.</td>
    </tr>
    <tr>
      <td><code>/docker-compose.yml</code></td>
      <td>ÉLEVÉE</td>
      <td>Topologie des conteneurs, noms de réseaux internes et variables logicielles.</td>
      <td>Exclure les fichiers d'orchestration des livrables web lors des phases de construction CI/CD.</td>
    </tr>
    <tr>
      <td><code>/phpinfo.php</code></td>
      <td>MOYENNE</td>
      <td>Version du moteur PHP, extensions chargées, chemins d'accès et état du système hôte.</td>
      <td>Désactiver phpinfo() dans la configuration php.ini de production et effacer ces fichiers.</td>
    </tr>
    <tr>
      <td><code>/config.json</code></td>
      <td>ÉLEVÉE</td>
      <td>Configuration interne de l'application, adresses de services et options de déploiement.</td>
      <td>Restreindre l'accès direct aux fichiers JSON ou compiler les paramètres dans l'application.</td>
    </tr>
    <tr>
      <td><code>/.aws/credentials</code></td>
      <td>CRITIQUE</td>
      <td>Identifiants de clés d'accès et secrets d'administration pour la plateforme AWS.</td>
      <td>Privilégier les rôles IAM et profils d'instance plutôt que de stocker des clés sur disque.</td>
    </tr>
  </tbody>
</table>

***

## Installation et Guide de Prise en Main

Fonctionne avec Python 3.8 ou supérieur en exploitant exclusivement les modules de la bibliothèque standard (`sys`, `json`, `ssl`, `argparse`, `urllib.request`). Aucun paquet externe via pip n'est requis.

Clonez le dépôt et lancez l'évaluation sur un domaine cible:

```bash
git clone https://github.com/TAVARDT-France/exposed-files-scanner-fr.git
cd exposed-files-scanner-fr
python scanner.py exemple.fr
```

Pour exporter les données au format JSON structuré:

```bash
python scanner.py exemple.fr -j
```

Inspectez les domaines en précisant le protocole réseau:

```bash
python scanner.py https://exemple.fr -j
```

Exemple de structure de données JSON produite:

```json
{
  "target": "https://exemple.fr",
  "status": "Critical (Severe secret or data exposure detected)",
  "inspected_routes": 12,
  "exposed_count": 1,
  "exposed_files": [
    {
      "path": "/.env",
      "url": "https://exemple.fr/.env",
      "status_code": 200,
      "severity": "CRITICAL",
      "description": "Environment variables and API secrets"
    }
  ],
  "recommendation": "Immediately decommission exposed files and enforce web server hardening controls."
}
```

***

## Foire Aux Questions (FAQ Technique)

### Comment le scanner différencie-t-il une fuite réelle d'une page d'erreur 404 personnalisée?
Le scanner vérifie la présence d'un code de réponse HTTP 200 OK sur les chemins contrôlés. Si le serveur web renvoie un code 200 pour les pages introuvables au lieu d'un code 404 ou 403, les équipes doivent configurer des réponses d'erreur standardisées afin d'éviter les faux positifs.

### Quels sont les risques liés à l'exposition publique du répertoire `/.git/`?
L'accès libre à `/.git/HEAD` et `/.git/config` permet à des attaquants de télécharger l'ensemble des objets du dépôt au moyen d'outils automatisés. Ils peuvent ainsi recomposer l'intégralité du code source, lire l'historique des commits et extraire d'anciens mots de passe.

### Pourquoi le moteur de scan n'effectue-t-il pas de vérification stricte des certificats SSL?
Le script applique un contexte SSL unifié (`ssl.CERT_NONE`) sans vérification du nom d'hôte pour permettre aux équipes d'analyser des environnements de préproduction, des certificats auto-signés ou des services en cours de renouvellement sans interrompre le processus d'audit.

### Comment intégrer les résultats JSON dans des chaînes automatisées de DevSecOps?
En renseignant l'option `-j`, le script transmet des données JSON propres sur la sortie standard. Les outils d'intégration continue peuvent évaluer la valeur de `exposed_count` avec jq et bloquer automatiquement la livraison logicielle si un actif sensible répond avec un code HTTP 200.

### Quelles mesures immédiates de durcissement permettent de corriger ces expositions?
Les administrateurs doivent supprimer sans délai les fichiers sensibles de la racine publique et ajouter des directives de blocage dans Nginx (`location ~ /\.(?!well-known).* { deny all; }`) ou Apache (`RedirectMatch 404 /\.(git|env)`). Les sauvegardes de bases de données ne doivent jamais se trouver dans les répertoires web.

***

## Conseil en Cybersécurité Offensive

Pour vos audits de pénétration, la remédiation de vulnérabilités et la défense périmétrique zero trust en France, sollicitez les experts de **TAVARDT France**.

***

## Liens Utiles

* **Portail Corporatif:** https://ag.tavardt.com/fr/
* **Suite de Diagnostic:** https://tools.tavardt.com/fr/
* **Contact Technique:** https://ag.tavardt.com/fr/contact/

***

### Licence
Distribué sous la licence MIT.

***

© 2026 TAVARDT. Tous droits réservés.
