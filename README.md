# SentimentAI

API REST simple d'analyse de sentiments pour des textes courts, développée avec FastAPI et Python.

## Fonctionnalités

- Analyse de texte et classification en trois catégories : POSITIVE, NEGATIVE ou NEUTRAL
- Score de confiance borné entre 0 et 1
- Endpoint de healthcheck pour Docker et les contrôles d'intégrité
- Exécution locale ou via Docker Compose

## Installation

1. Cloner le repository

```bash
git clone https://github.com/VOTRE_PSEUDO/sentiment-ai.git
cd sentiment-ai
```

2. Installer les dépendances

```bash
pip install -r requirements.txt
```

## Utilisation

### Mode développement

```bash
uvicorn src.main:app --reload
```

### Mode production avec Docker

```bash
docker compose up -d
```

### Tests

```bash
make test
```

## Endpoints

### GET /health

Endpoint de healthcheck

```bash
curl http://localhost:8000/health
```

### POST /predict

Analyse le sentiment du texte

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "Ce produit est excellent !"}'
```

Réponse attendue:

```json
{
  "label": "POSITIVE",
  "score": 0.6,
  "text": "Ce produit est excellent !"
}
```

## Structure du projet

```
sentiment-ai/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── model.py
│   └── schemas.py
├── tests/
│   ├── __init__.py
│   └── test_api.py
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── requirements.txt
└── README.md
```

## Commandes Makefile

- `make build` : construire l'image Docker
- `make run` : démarrer la stack Docker Compose
- `make test` : exécuter les tests dans Docker
- `make stop` : arrêter la stack
- `make clean` : nettoyer les conteneurs et l'image
- `make tag` : créer un tag Git

## Jenkins

Le fichier [Jenkinsfile](Jenkinsfile) décrit un pipeline CI simple en trois étapes : récupération du code, construction de l'image Docker et exécution des tests dans le conteneur.

Pour l’utiliser dans Jenkins :

1. Créez un pipeline job ou un multibranch pipeline.
2. Choisissez une source Git qui pointe vers ce dépôt.
3. Vérifiez que le job lit le [Jenkinsfile](Jenkinsfile) à la racine du projet.
4. Installez les plugins suggérés par Jenkins au premier démarrage, puis ajoutez au besoin `Pipeline`, `Git` et `Docker Pipeline`.

Le pipeline archive aussi les rapports de test et de couverture dans `reports/`.

## Licence

MIT

