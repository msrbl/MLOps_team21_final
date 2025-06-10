pipeline {
    agent {
        docker {
            image 'python:3.11-slim'
            args  '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    environment {
        DOCKER_IMAGE_NAME = 'team21/model'
        DOCKER_IMAGE_TAG  = "${env.BUILD_NUMBER}"
        DOCKER_REGISTRY   = 'docker.io'
    }
    stages {
        stage('Setup Python venv') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Lint') {
            steps {
                echo '=== Running Linting ==='
                sh '''
                    dvc pull
                    black --check src tests
                    mypy src tests
                '''
            }
        }

        stage('Train Model') {
            steps {
                echo '=== Training Model ==='
                sh '''
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                    dvc pull
                    python -m src.services.model_pipeline.pipeline
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'models/**', fingerprint: true
                }
            }
        }

        stage('Test') {
            steps {
                echo '=== Running Tests ==='
                sh '''
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                    dvc pull
                    pytest tests/
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE_NAME:$DOCKER_IMAGE_TAG .'
            }
        }

        stage('Deploy') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-credentials',
                                                    usernameVariable: 'DOCKER_USER',
                                                    passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker tag $DOCKER_IMAGE_NAME:$DOCKER_IMAGE_TAG $DOCKER_REGISTRY/$DOCKER_IMAGE_NAME:$DOCKER_IMAGE_TAG
                        docker push $DOCKER_REGISTRY/$DOCKER_IMAGE_NAME:$DOCKER_IMAGE_TAG
                    '''
                }
            }
        }
  }
  post {
    always {
      archiveArtifacts artifacts: 'data/processed/**/*', fingerprint: true
    }
  }
}