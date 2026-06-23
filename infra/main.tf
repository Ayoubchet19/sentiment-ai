terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

# Windows avec Docker Desktop
provider "docker" {
  host = "npipe:////./pipe/docker_engine"
}

# Reseau Docker partage Jenkins / SonarQube / SentimentAI
# Ce reseau existe deja depuis le TP2/TP3 -- voir Partie 3.1
resource "docker_network" "cicd" {
  name = "cicd-network"
}

# Image Docker SentimentAI -- image LOCALE buildee par Jenkins
resource "docker_image" "sentiment" {
  name         = "sentiment-ai:${var.image_tag}"
  keep_locally = true
}

# Conteneur staging
resource "docker_container" "sentiment_staging" {
  name  = "sentiment-staging"
  image = docker_image.sentiment_ai.name

  restart {
    name = "unless-stopped"
  }

  ports {
    internal = 8001
    external = 8001
  }
}
