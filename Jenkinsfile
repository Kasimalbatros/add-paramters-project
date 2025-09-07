pipeline {
    agent any

    parameters {
        choice(name: 'ENV', choices: ['DEV', 'QA', 'PROD'], description: 'Select the environment')
        string(name: 'BRANCH', defaultValue: 'main', description: 'Git branch to build')
        string(name: 'GIT_URL', defaultValue: 'https://github.com/your-username/your-repo-name.git', description: 'Git repository URL')
    }

    environment {
        DEV_URL  = "http://dev.example.com"
        QA_URL   = "http://qa.example.com"
        PROD_URL = "http://prod.example.com"
        DOCKER_IMAGE = "my-python-app:${env.BUILD_ID}"
    }

    stages {
        stage('Checkout') {
            steps {
                echo "Fetching code from ${params.GIT_URL} on branch ${params.BRANCH}"
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: "*/${params.BRANCH}"]],
                    extensions: [],
                    userRemoteConfigs: [[url: "${params.GIT_URL}"]]
                ])
            }
        }

        stage('Build') {
            steps {
                echo "Building application for ${params.ENV} environment"
                // Build your Docker image
                sh "docker build -t ${DOCKER_IMAGE} ."
            }
        }

        stage('Test') {
            steps {
                echo "Running tests"
                // Example: Run your tests
                sh "python -m pytest tests/ || true" // Continue even if tests fail
            }
        }

        stage('Deploy') {
            steps {
                script {
                    // Define environment configuration within script block
                    def envConfig = [
                        'DEV': [url: DEV_URL, port: 5001, env: 'development'],
                        'QA': [url: QA_URL, port: 5002, env: 'testing'], 
                        'PROD': [url: PROD_URL, port: 5003, env: 'production']
                    ]
                    
                    def config = envConfig[params.ENV]
                    
                    echo "Deploying to ${config.url}"
                    echo "Using port: ${config.port}"
                    
                    // Example deployment command
                    sh """
                        docker run -d \
                        --name my-app-${params.ENV.toLowerCase()} \
                        -p ${config.port}:5000 \
                        -e ENVIRONMENT=${config.env} \
                        ${DOCKER_IMAGE}
                    """
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline finished for ${params.ENV}"
            // Clean up Docker containers
            sh "docker ps -aq --filter name=my-app- | xargs --no-run-if-empty docker rm -f || true"
        }
        success {
            echo "Pipeline completed successfully!"
        }
        failure {
            echo "Pipeline failed!"
        }
    }
}
