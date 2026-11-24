# Scanner de Fichiers et Identifiants Exposés

[![Scanner Fichiers Exposes](https://img.shields.io/badge/TAVARDT-Surface%20Attaque-5b3cf5.svg)](https://tools.tavardt.com/fr/scanner-fichiers-exposes/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)

Scanner de surface d attaque pour la detection automatisee de fichiers d environnement, sauvegardes de bases de donnees et metadonnees git exposees.

Developpe et maintenu par la division de cybersecurite offensive de **TAVARDT**.

***

## Perimetre de Detection de Surface

* **Variables d Environnement et Secrets**: Inspection des fichiers `.env`, `.env.local` et `.env.production`.
* **Metadonnees de Versionnement**: Detection des repertoires exposes `/.git/HEAD` et `/.git/config`.
* **Sauvegardes de Bases de Donnees**: Identification des exports SQL sensibles tels que `backup.sql` et `dump.sql`.
* **Infrastructure et Orchestration**: Analyse des fichiers `docker-compose.yml` et des divulgations via `phpinfo.php`.
* **Conformite Normative**: Aligne sur les recommandations du Recommandations de Securite de l ANSSI et RGPD (CNIL).

***

## Installation et Utilisation

Fonctionne avec Python 3.8 ou superieur, sans bibliotheque externe.

```bash
git clone https://github.com/TAVARDT-France/exposed-files-scanner-fr.git
cd exposed-files-scanner-fr
python scanner.py entreprise.fr
```

Pour exporter les resultats en JSON:

```bash
python scanner.py entreprise.fr -json
```

***

## Diagnostic Web en Ligne

Pour des analyses graphiques et un suivi continu du perimetre, consultez l outil officiel:

* **Scanner de Fichiers Exposes**
* **[Portail Entreprise TAVARDT](https://ag.tavardt.com/fr/)**

***

## Conseil en Cybersecurite Offensive

Pour vos audits de penetration et la reduction de votre surface d attaque en France, sollicitez les experts de **TAVARDT**.

***

## Liens Utiles

* **Portail Entreprise:** https://ag.tavardt.com/fr/
* **Suite de Diagnostic:** https://tools.tavardt.com/fr/
* **Contact Technique:** https://ag.tavardt.com/fr/contact/

***

© 2026 TAVARDT. Tous droits réservés.
