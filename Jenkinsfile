pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = "y30308/django-app"
        IMAGE_TAG = "${BUILD_NUMBER}"
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        GIT_CREDENTIALS = credentials('github-credentials')
        MANIFEST_REPO = "https://github.com/Jyn-K/django-k8s-manifests.git"
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Test') {
            steps {
                sh '''
                    python -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                    python manage.py test
                '''
            }
        }
        
        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t ${DOCKER_IMAGE}:${IMAGE_TAG} .
                    docker tag ${DOCKER_IMAGE}:${IMAGE_TAG} ${DOCKER_IMAGE}:latest
                '''
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                sh '''
                    echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin
                    docker push ${DOCKER_IMAGE}:${IMAGE_TAG}
                    docker push ${DOCKER_IMAGE}:latest
                '''
            }
        }
        
        stage('Update Kubernetes Manifest') {
            steps {
                sh '''
                    rm -rf manifest-repo
                    git clone ${MANIFEST_REPO} manifest-repo
                    cd manifest-repo
                    sed -i "s|image:.*django-app.*|image: ${DOCKER_IMAGE}:${IMAGE_TAG}|g" django-deployment.yaml
                    git config user.email "jenkins@example.com"
                    git config user.name "Jenkins"
                    git add django-deployment.yaml
                    git commit -m "Update image to ${IMAGE_TAG}"
                    git push https://${GIT_CREDENTIALS_USR}:${GIT_CREDENTIALS_PSW}@github.com/Jyn-K/django-k8s-manifests.git main
                '''
            }
        }
    }
    
    post {
        always {
            sh 'docker logout'
        }
    }
}
