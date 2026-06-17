# SentimentAI

API REST d'analyse de sentiments pour les avis clients, développée en FastAPI/Python.

## Fonctionnalités

- Analyse de texte et classification en trois catégories : POSITIF, NÉGATIF ou NEUTRE
- Score de confiance accompagnant chaque prédiction
- Endpoint de healthcheck pour les conteneurs et load balancers
- Conteneurisée avec Docker et Docker Compose

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

### Mode production (avec Docker)

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
  "score": 0.7,
  "text": "Ce produit est excellent !"
}
```

## Structure du projet

```
sentiment-ai/
├── src/
│   ├── __init__.py
│   ├── main.py           # Application FastAPI
│   ├── model.py          # Modèle de sentiment
│   └── schemas.py        # Schémas Pydantic
├── tests/
│   ├── __init__.py
│   └── test_api.py       # Tests unitaires
├── Dockerfile            # Configuration Docker
├── docker-compose.yml    # Orchestration des conteneurs
├── Makefile              # Automatisation des tâches
├── requirements.txt      # Dépendances Python
└── README.md             # Ce fichier
```

## Commandes Makefile

- `make build` : Construire l'image Docker
- `make run` : Démarrer la stack Docker Compose
- `make test` : Exécuter les tests dans Docker
- `make stop` : Arrêter la stack
- `make clean` : Nettoyer les conteneurs et images
- `make tag` : Créer un tag Git

## Licence

MIT
