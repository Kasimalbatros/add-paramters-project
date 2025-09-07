pipeline {
    agent any

    parameters {
        choice(name: 'ENV', choices: ['DEV', 'QA', 'PROD'], description: 'Select the environment')
    }

    environment {
        DOCKER_IMAGE = "my-python-app:${env.BUILD_ID}"
        DEV_URL  = "http://dev.example.com"
        QA_URL   = "http://qa.example.com"
        PROD_URL = "http://prod.example.com"
        
        // Environment-specific variables
        ENV_VARS = [
            DEV: [ENVIRONMENT: 'development', PORT: 5001],
            QA:  [ENVIRONMENT: 'testing', PORT: 5002],
            PROD: [ENVIRONMENT: 'production', PORT: 5003]
        ]
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Test') {
            steps {
                sh 'python -m pytest tests/ -v'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image for ${params.ENV} environment"
                    sh "docker build -t ${DOCKER_IMAGE} ."
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    def envVars = ENV_VARS[params.ENV]
                    
                    echo "Deploying to ${params.ENV} environment"
                    
                    if (params.ENV == 'DEV') {
                        echo "Deploying to Development at ${DEV_URL}"
                        sh """
                            docker run -d \
                            --name my-python-app-${params.ENV.toLowerCase()} \
                            -p ${envVars.PORT}:5000 \
                            -e ENVIRONMENT=${envVars.ENVIRONMENT} \
                            ${DOCKER_IMAGE}
                        """
                    }
                    else if (params.ENV == 'QA') {
                        echo "Deploying to QA at ${QA_URL}"
                        sh """
                            docker run -d \
                            --name my-python-app-${params.ENV.toLowerCase()} \
                            -p ${envVars.PORT}:5000 \
                            -e ENVIRONMENT=${envVars.ENVIRONMENT} \
                            ${DOCKER_IMAGE}
                        """
                    }
                    else if (params.ENV == 'PROD') {
                        echo "Deploying to Production at ${PROD_URL}"
                        sh """
                            docker run -d \
                            --name my-python-app-${params.ENV.toLowerCase()} \
                            -p ${envVars.PORT}:5000 \
                            -e ENVIRONMENT=${envVars.ENVIRONMENT} \
                            ${DOCKER_IMAGE}
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline finished for ${params.ENV}"
            // Clean up - remove stopped containers
            sh 'docker ps -aq --filter status=exited | xargs -r docker rm'
        }
        success {
            echo "Pipeline succeeded!"
        }
        failure {
            echo "Pipeline failed!"
        }
    }
}
