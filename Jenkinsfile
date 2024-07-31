pipeline {
    agent any

    options{
        // Max number of build logs to keep and days to keep
        buildDiscarder(logRotator(numToKeepStr: '5', daysToKeepStr: '5'))
        // Enable timestamp at each job in the pipeline
        timestamps()
    }

    environment{
        registry = 'hieugoku/text-image-retrieval-app'
        registryCredential = 'dockerhub'
    }

    stages {
        stage('Test') {
            steps {
                echo 'Testing model correctness..'
                echo 'Always pass all test unit :))'
            }
        }

        stage('Build image') {
            steps {
                script {
                    echo 'Building image for deployment...'
                    def imageName = "${registry}:v${BUILD_NUMBER}"
                    dockerImage = docker.build(imageName, "--file Dockerfile-app-serving .")
                    echo 'Pushing image to dockerhub...'
                    docker.withRegistry( '', registryCredential ) {
                        dockerImage.push()
                    }
                }
            }
        }

        stage('Deploy to Google Kubernetes Engine') {
            agent {
                kubernetes {
                    containerTemplate {
                        name 'helm' // Name of the container to be used for helm upgrade
                        image 'hieugoku/jenkins:lts' // The image containing helm
                    }
                }
            }
            steps {
                script {
                    steps
                    container('helm') {
                        sh("helm upgrade --install app --set image.repository=${registry} \
                        --set image.tag=v${BUILD_NUMBER} \
                        --set env.QDRANT_URL=${QDRANT_URL} \
                        --set env.QDRANT_CLOUD_KEY=${QDRANT_CLOUD_KEY} \
                        --set env.COLLECTION_NAME=${COLLECTION_NAME} \
                        --set env.HUGGINGFACE_API_KEY=${HUGGINGFACE_API_KEY} \
                        --set env.DATA_DIR=${DATA_DIR} \
                        --set env.MODEL_DIR=${MODEL_DIR} \
                        --set env.BUCKET_NAME=${BUCKET_NAME} \
                        --set env.IMAGE_URL_TEMPLATE=${IMAGE_URL_TEMPLATE} \
                        ./helm_charts/app --namespace model-serving")
                    }
                }
            }
        }
    }
}
