pipeline {
    agent {
        docker {
        image 'python:3.11-slim'
        args  '--network host \
                --user 0:0 \
                -e HOME=/root \
                -v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    environment {
        HOME              = '/root'  
        DOCKER_IMAGE_NAME = 'team21/model'
        DOCKER_IMAGE_TAG  = "${env.BUILD_NUMBER}"
        DOCKER_REGISTRY   = 'docker.io'
    }
    stages {
        stage('Setup Python venv') {
            steps {
                sh '''
                    set -e
                    python -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip --no-cache-dir
                    pip install -r requirements.txt --no-cache-dir
                    pip install --no-cache-dir -e .
                '''
            }
        }

        // stage('Lint') {
        //     steps {
        //         echo '=== Running Linting ==='
        //         withCredentials([file(credentialsId: 'gdrive-sa', variable: 'SA_JSON')]) {
        //             sh '''
        //                 set -e
        //                 . venv/bin/activate

        //                 black src tests
        //                 mypy src tests
        //             '''
        //         }
        //     }
        // }

        stage('Train Model') {
            steps {
                echo '=== Training Model ==='
                withCredentials([file(credentialsId: 'gdrive-sa', variable: 'SA_JSON')]) {
                    sh '''
                        set -e
                        . venv/bin/activate
                        
                        dvc remote modify --local myremote gdrive_service_account_json_file_path "$SA_JSON"
                        dvc pull
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

        stage('Test') {
            steps {
                echo '=== Running Tests ==='
                withCredentials([file(credentialsId: 'gdrive-sa', variable: 'SA_JSON')]) {
                    sh '''
                        set -e
                        . venv/bin/activate
                        
                        dvc remote modify --local myremote gdrive_service_account_json_file_path "$SA_JSON"
                        dvc pull
                        pytest tests/

                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.image('docker:24').inside(
                        '--network host -e HOME=/root -v /var/run/docker.sock:/var/run/docker.sock'
                    ) {
                        sh "docker build -t ${DOCKER_REGISTRY}/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG} ."
                    }
                }
            }
        }
        stage('Deploy') {
             steps {
                script {
                    docker.image('docker:24').inside(
                        '--network host -e HOME=/root -v /var/run/docker.sock:/var/run/docker.sock'
                    ) {
                        docker.withRegistry("https://${DOCKER_REGISTRY}", 'docker-credentials') {
                            sh "docker push ${DOCKER_REGISTRY}/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}"
                            sh """
                                docker tag ${DOCKER_REGISTRY}/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG} \
                                        ${DOCKER_REGISTRY}/${DOCKER_IMAGE_NAME}:latest
                                docker push ${DOCKER_REGISTRY}/${DOCKER_IMAGE_NAME}:latest
                            """
                        }
                    }
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