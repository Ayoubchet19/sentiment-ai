pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    environment {
        IMAGE_NAME = 'sentiment-ai'
        REGISTRY = 'ghcr.io/ayoubchet19'
        IMAGE_TAG = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                echo "Branche : ${env.BRANCH_NAME}"
                echo "Commit : ${env.GIT_COMMIT}"
            }
        }

        stage('Lint') {
            steps {
                sh '''
docker run --rm \
    --volumes-from jenkins \
    -w $WORKSPACE \
    python:3.12-slim \
    sh -c "pip install flake8 -q && flake8 src/ --max-line-length=100"
'''
            }
        }

    stage('IaC Validate') {
        steps {
            dir('infra') {
                sh """
                    docker run --rm \
                        -v \$PWD:/workspace \
                        -w /workspace \
                        hashicorp/terraform:1.9.8 \
                        terraform init -backend=false -input=false
                """
            }
        }
    }



        stage('Build & Test') {
            steps {
                sh '''
docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .

# Supprimer un éventuel conteneur test-runner résiduel
docker rm -f test-runner 2>/dev/null || true

# Lancer les tests en nommant le conteneur pour copier coverage.xml
set +e
docker run \
    -e CI=true \
    --name test-runner \
    ${IMAGE_NAME}:${IMAGE_TAG} \
    pytest tests/ -v \
    --cov=src \
    --cov-report=xml:/tmp/coverage.xml \
    --cov-report=term-missing \
    --cov-fail-under=70
TEST_EXIT_CODE=$?
set -e

# Copier coverage.xml depuis le conteneur vers le workspace
docker cp test-runner:/tmp/coverage.xml ./coverage.xml 2>/dev/null || true
docker rm -f test-runner 2>/dev/null || true

# Retourner le code de sortie des tests
exit $TEST_EXIT_CODE
'''
            }
            post {
                failure { echo 'Tests échoués ou coverage insuffisant (< 70%)' }
            }
        }

        stage('SonarQube Analysis') {
            environment {
                SONARQUBE_TOKEN = credentials('sonar-token')
            }
            steps {
                withSonarQubeEnv('sonarqube') {
                    sh '''
docker run --rm \
    --network cicd-network \
    --volumes-from jenkins \
    -w "$WORKSPACE" \
    -e SONAR_HOST_URL="$SONAR_HOST_URL" \
    -e SONAR_TOKEN="$SONARQUBE_TOKEN" \
    sonarsource/sonar-scanner-cli:latest \
    sonar-scanner \
    -Dsonar.projectKey=sentiment-ai \
    -Dsonar.projectName=SentimentAI \
    -Dsonar.projectBaseDir="$WORKSPACE" \
    -Dsonar.sources=src \
    -Dsonar.python.version=3.11 \
    -Dsonar.python.coverage.reportPaths=coverage.xml \
    -Dsonar.sourceEncoding=UTF-8 \
    -Dsonar.scanner.metadataFilePath=$WORKSPACE/report-task.txt
'''
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 15, unit: 'MINUTES') {
                    // Attend le résultat asynchrone du Quality Gate SonarQube
                    // abortPipeline: true => bloque Push et Deploy si le gate échoue
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Security Scan') {
            steps {
                sh '''
docker run --rm \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v trivy-cache:/root/.cache/trivy \
    aquasec/trivy:latest image \
    --severity HIGH,CRITICAL \
    --exit-code 1 \
    --format table \
    ${IMAGE_NAME}:${IMAGE_TAG}
'''
            }
            post {
                failure {
                    echo 'Vulnérabilités CRITICAL ou HIGH détectées !'
                    echo 'Corrigez les dépendances avant de déployer.'
                }
            }
        }

        stage('Push') {
            when { branch 'main' }
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'github-token',
                    usernameVariable: 'REGISTRY_USER',
                    passwordVariable: 'REGISTRY_PASS'
                )]) {
                    sh """
echo \$REGISTRY_PASS | docker login ghcr.io \
    -u \$REGISTRY_USER --password-stdin
docker push ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}
"""
                }
            }
        }

        stage('IaC Apply') {
            when { branch 'main' }
            steps {
                dir('infra') {
                    sh 'terraform init -input=false'
                    sh """
terraform apply -auto-approve \
    -var='image_tag=${IMAGE_TAG}'
"""
                }
            }
        }

        stage('Deploy Staging') {
            when { branch 'main' }
            steps {
                sh 'curl -f http://localhost:8001/health || exit 1'
            }
        }
    }

    post {
        always {
            sh 'docker compose down -v 2>/dev/null || true'
        }
        success {
            echo "Pipeline OK -- ${IMAGE_TAG} deploye"
        }
        failure {
            echo 'Pipeline KO'
        }
    }
}