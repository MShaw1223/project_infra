pipeline {
    agent any
    parameters {
        string(name: 'PUBLIC_IP', description: 'Public IP address of the server')
    }
    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'prod', url: 'https://github.com/adampalmergithub/addressBook.git'
            }
        }
        stage('Build') {
            steps {
                sh 'docker-compose down --volumes --remove-orphans'
                sh 'docker-compose build --no-cache'
            }
        }
        stage('Run') {
            steps {
                sh 'docker-compose up -d'
            }
        }
        stage('Health Check') {
            steps {
                script {
                    sleep(10)
                    def response = sh(script: "curl -s -o /dev/null -w '%{http_code}' http://${params.PUBLIC_IP}", returnStdout: true).trim()
                    if (response != '200') {
                        error("Application is not responding correctly. Received HTTP ${response}")
                    }
                }
            }
        }
    }
    post {
        always {
            sh 'docker-compose logs'
        }
        failure {
            sh 'docker-compose down'
        }
    }
}
