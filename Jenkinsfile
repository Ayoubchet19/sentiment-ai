pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    environment {
        IMAGE_NAME = 'sentiment-ai'
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'git rev-parse --short HEAD'
            }
        }

        stage('Build image') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .'
            }
        }

        stage('Test') {
            steps {
                sh '''
mkdir -p reports
docker run --rm \
    -v "$WORKSPACE:/app" \
    -w /app \
    ${IMAGE_NAME}:${IMAGE_TAG} \
    pytest tests/ -v \
    --cov=src \
    --cov-report=term-missing \
    --cov-report=xml:reports/coverage.xml \
    --junitxml=reports/junit.xml
'''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
            sh 'docker image rm -f ${IMAGE_NAME}:${IMAGE_TAG} >/dev/null 2>&1 || true'
        }
        success {
            echo 'Pipeline Jenkins réussie.'
        }
        failure {
            echo 'Pipeline Jenkins échouée. Vérifiez les logs de test ou la construction Docker.'
        }
    }
}