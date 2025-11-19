pipeline {
    agent any
    environment {
        DOCKER_IMAGE = "y30308/django-app"
        IMAGE_TAG = "${BUILD_NUMBER}"
    }
    stages {
        stage('Test') {
            agent {
                docker {
                    image 'python:3.9'
                }
            }
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                    cd mysite
                    python manage.py test
                '''
            }
        }
        stage('Setup Buildx') {
            steps {
                sh '''
                    docker buildx create --use --name mybuilder || docker buildx use mybuilder
                    docker buildx inspect --bootstrap
                '''
            }
        }
        stage('Build & Push') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    sh '''
                        echo $PASS | docker login -u $USER --password-stdin
                        docker buildx build --platform linux/amd64,linux/arm64 \
                            -t ${DOCKER_IMAGE}:${IMAGE_TAG} \
                            -t ${DOCKER_IMAGE}:latest \
                            --push .
                    '''
                }
            }
        }
        stage('Update Manifest') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'github-credentials', usernameVariable: 'USER', passwordVariable: 'TOKEN')]) {
                    sh """
                        rm -rf django-k8s-manifests
                        git clone https://${TOKEN}@github.com/Jyn-K/django-k8s-manifests
                        cd django-k8s-manifests
                        sed -i 's|image: ${DOCKER_IMAGE}:.*|image: ${DOCKER_IMAGE}:${IMAGE_TAG}|' django-deployment.yaml
                        git config user.email "jenkins@example.com"
                        git config user.name "Jenkins"
                        git commit -am 'Update image to ${IMAGE_TAG}'
                        git push
                    """
                }
            }
        }
    }
}
