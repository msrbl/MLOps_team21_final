pipeline {
    agent none

    options {
        ansiColor('xterm')
        timestamps()
        disableConcurrentBuilds()
        skipStagesAfterUnstable()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    environment {
        DOCKER_IMAGE_NAME = 'team21/model'
        DOCKER_IMAGE_TAG  = "${env.BUILD_NUMBER}"
        DOCKER_REGISTRY   = 'docker.io'

        GDRIVE_CREDENTIALS_ID = 'gdrive-sa'
    }

    stages {

        stage('Checkout') {
            agent any
            steps {
                checkout scm
            }
        }

        stage('Setup & Cache') {
            agent {
                docker {
                    image 'python:3.11-slim'
                    args  '--network host \
                           -v $HOME/.cache/pip:/root/.cache/pip'
                }
            }
            options {
                cache(paths: ['venv/', '/root/.cache/pip'], key: "pip-${env.GIT_COMMIT}")
            }
            steps {
                sh '''
                    python -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install -e .
                '''
                stash includes: 'venv/**', name: 'venv'
            }
        }

        stage('Lint & Test') {
            parallel {
                stage('Lint') {
                    agent {
                        docker { image 'python:3.11-slim'; args '--network host' }
                    }
                    steps {
                        unstash 'venv'
                        sh '''
                            . venv/bin/activate
                            black src tests
                            mypy src tests
                        '''
                    }
                }
                stage('Unit Tests') {
                    agent {
                        docker { image 'python:3.11-slim'; args '--network host' }
                    }
                    steps {
                        unstash 'venv'
                        withCredentials([file(credentialsId: "${GDRIVE_CREDENTIALS_ID}", variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                            sh '''
                                . venv/bin/activate
                                dvc pull --jobs 4
                                pytest --maxfail=1 --disable-warnings -q /tests/test_data_quality.py
                            '''
                        }
                    }
                }
            }
        }

        stage('Train Model') {
            agent {
                docker { image 'python:3.11-slim'; args '--network host' }
            }
            steps {
                unstash 'venv'
                withCredentials([file(credentialsId: "${GDRIVE_CREDENTIALS_ID}", variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    sh '''
                        . venv/bin/activate
                        dvc pull --jobs 4
                        python -m src.services.model_pipeline.pipeline
                    '''
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'models/**', fingerprint: true
                }
            }
        }

        stage('Integration Tests') {
            agent {
                docker { image 'python:3.11-slim'; args '--network host' }
            }
            steps {
                unstash 'venv'
                withCredentials([file(credentialsId: "${GDRIVE_CREDENTIALS_ID}", variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    sh '''
                        . venv/bin/activate
                        dvc pull --jobs 4
                        pytest --maxfail=1 --disable-warnings -q /tests/test_endpoints.py
                    '''
                }
            }
        }

        stage('Build & Push Docker') {
            agent {
                docker {
                    image 'docker:23.0-dind'
                    args  '--privileged --network host'
                }
            }
            steps {
                script {
                    docker.withRegistry("https://${DOCKER_REGISTRY}", "${DOCKER_CREDENTIALS_ID}") {
                        def img = docker.build("${DOCKER_REGISTRY}/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}")
                        img.push()
                        img.push('latest')
                    }
                }
            }
        }
    }
    post {
        success {
            echo '✅ Сборка успешно завершена'
        }
        failure {
            echo '❌ Сборка упала'
        }
        always {
            archiveArtifacts artifacts: 'data/processed/**/*', fingerprint: true
        }
    }
}