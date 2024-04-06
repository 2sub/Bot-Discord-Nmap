# Bot-Discord-Nmap

## Aide Commande

Ce bot Discord est conçu pour fournir des fonctionnalités telles que le scan Nmap, le ping et le scan HTTP. Voici comment vous pouvez l'utiliser:

### Installation

1. télécharger les fichier sur votre pc.
2. Assurez-vous que vous avez Python installé.
3. Installez les modules dans requirment.txt
4. ils vous faudra nmap installé sur votre pc pour héberger le bot

### Configuration

1. Créez une application et un bot Discord sur le [portail des développeurs Discord](https://discord.com/developers/applications).
2. Copiez le jeton (token) du bot.
3. Puis remplacer TOKEN par le token de votre bot discord

### Utilisation

Une fois que le bot est installé et configuré, vous pouvez l'exécuter en exécutant le fichier `bot-nmap.py`. Le bot utilisera le préfixe `!` pour toutes les commandes. Voici quelques exemples de commandes que vous pouvez utiliser :

- `!nmap [ip]` : Effectue un scan Nmap sur l'adresse IP fournie.
- `!ping [ip]` : Effectue un ping vers l'adresse IP fournie.
- `!scan [url]` : Effectue un scan HTTP sur l'URL fournie.
