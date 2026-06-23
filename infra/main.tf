terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {}

variable "image_tag" {
  type = string
}

resource "docker_image" "sentiment_ai" {
  name = "sentiment-ai:${var.image_tag}"

  build {
    context    = "../"
    dockerfile = "../Dockerfile"
  }
}

resource "docker_container" "sentiment_staging" {
  name  = "sentiment-staging"
  image = docker_image.sentiment_ai.name



  ports {
    internal = 8001
    external = 8001
  }
}
