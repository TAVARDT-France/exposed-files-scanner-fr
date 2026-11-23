#!/usr/bin/env python3
import sys
import json
import ssl
import argparse
import urllib.request

SENSITIVE_PATHS = [
    {"path": "/.env", "severity": "CRITICAL", "description": "Environment variables and API secrets"},
    {"path": "/.env.local", "severity": "CRITICAL", "description": "Local environment variables"},
    {"path": "/.env.production", "severity": "CRITICAL", "description": "Production environment secrets"},
    {"path": "/.git/HEAD", "severity": "CRITICAL", "description": "Source code repository metadata"},
    {"path": "/.git/config", "severity": "CRITICAL", "description": "Git remote repository configuration"},
    {"path": "/backup.sql", "severity": "CRITICAL", "description": "Database SQL dump"},
    {"path": "/dump.sql", "severity": "CRITICAL", "description": "Database export file"},
    {"path": "/database.sql", "severity": "CRITICAL", "description": "Raw SQL schema dump"},
    {"path": "/docker-compose.yml", "severity": "HIGH", "description": "Container orchestration configuration"},
    {"path": "/phpinfo.php", "severity": "MEDIUM", "description": "Server environment information disclosure"},
    {"path": "/config.json", "severity": "HIGH", "description": "Application configuration data"},
    {"path": "/.aws/credentials", "severity": "CRITICAL", "description": "Cloud provider access keys"}
]

def scan_target(target_url):
    if not target_url.startswith("http://") and not target_url.startswith("https://"):
        target_url = "https://" + target_url
    target_url = target_url.rstrip("/")

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    detected = []

    for item in SENSITIVE_PATHS:
        url = target_url + item["path"]
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "TAVARDT-ExposedFiles-Audit/1.0"})
            with urllib.request.urlopen(req, context=ctx, timeout=3) as resp:
                if resp.getcode() == 200:
                    detected.append({
                        "path": item["path"],
                        "url": url,
                        "status_code": 200,
                        "severity": item["severity"],
                        "description": item["description"]
                    })
        except Exception:
            pass

    return detected

def main():
    parser = argparse.ArgumentParser(description="TAVARDT France: Scanner de Fichiers Sensibles et d Identifiants Exposes")
    parser.add_argument("target", help="Target domain or base URL to inspect")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    args = parser.parse_args()

    target = args.target.strip()
    detected = scan_target(target)
    is_critical = len(detected) > 0
    status = "Critique (Exposition severe de donnees ou d identifiants)" if is_critical else "Securise (Aucun fichier sensible detecte)"

    if args.json:
        payload = {
            "target": target,
            "status": status,
            "inspected_routes": len(SENSITIVE_PATHS),
            "exposed_count": len(detected),
            "exposed_files": detected,
            "recommendation": "Supprimez immediatement les fichiers exposes et bloquez les acces via la configuration du serveur web ou WAF." if is_critical else "No immediate action required."
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return

    border = "=" * 76
    print(border)
    print(f" TAVARDT FRANCE: SCANNER DE FICHIERS SENSIBLES ET D IDENTIFIANTS EXPOSES")
    print(border)
    print(f" Target: {target}")
    print(f" Diagnostic General: {status}")
    print(f" Points de Controle Inspectes: {len(SENSITIVE_PATHS)}")
    print(f" Fichiers Exposes Detectes: {len(detected)}")
    print("-" * 76)
    if detected:
        for d in detected:
            print(f"   * [{d['severity']}] {d['path']} (HTTP 200) - {d['description']}")
        print("-" * 76)
        print(f" Recommandations de Securite:")
        print(f"   * Supprimez immediatement les fichiers exposes et bloquez les acces via la configuration du serveur web ou WAF.")
    else:
        print(f" Aucune exposition publique détectée sur les routes surveillées.")
    print(border)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Usage: python scanner.py <domain_or_url> [--json]")
        sys.exit(1)
    main()
