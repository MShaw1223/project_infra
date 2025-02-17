pipeline {
    agent any
    parameters {
        string(name: 'PUBLIC_IP', description: 'Public IP address of the EC2 server')
	string(name: 'SSH_CREDENTIALS_ID', defaultValue: 'ssh-key-jenkins-ec2', description: 'Jenkins SSH Key ID')
    }
    environment {
        EC2_USER = 'ec2-user'
        EC2_HOST = "${params.PUBLIC_IP}"
    }
    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    withCredentials([sshUserPrivateKey(credentialsId: params.SSH_CREDENTIALS_ID, keyFileVariable: 'SSH_KEY_PATH')]) {
                        sh """
                        ssh -o StrictHostKeyChecking=no -i ${SSH_KEY_PATH} ${EC2_USER}@${EC2_HOST} 'set -e; cd finalproj && docker-compose build --no-cache'
                        """
                    }
                }
            }
        }
        stage('Run Docker Containers') {
            steps {
                script {
                    withCredentials([sshUserPrivateKey(credentialsId: params.SSH_CREDENTIALS_ID, keyFileVariable: 'SSH_KEY_PATH')]) {
                        sh """
                        ssh -o StrictHostKeyChecking=no -i ${SSH_KEY_PATH} ${EC2_USER}@${EC2_HOST} 'set -e; cd finalproj && docker-compose up -d'
                        """
                    }
                }
            }
        }
        stage('Health Check') {
            steps {
                script {
                    withCredentials([sshUserPrivateKey(credentialsId: params.SSH_CREDENTIALS_ID, keyFileVariable: 'SSH_KEY_PATH')]) {
                        def response = sh(script: "ssh -o StrictHostKeyChecking=no -i ${SSH_KEY_PATH} ${EC2_USER}@${EC2_HOST} 'curl -s -o /dev/null -w \"%{http_code}\" http://localhost'", returnStdout: true).trim()
                        if (response != '200') {
                            error("Application is not responding correctly. Received HTTP ${response}")
                        }
                    }
                }
            }
        }
    }
    post {
        always {
            script {
                withCredentials([sshUserPrivateKey(credentialsId: params.SSH_CREDENTIALS_ID, keyFileVariable: 'SSH_KEY_PATH')]) {
                    sh """
                    ssh -o StrictHostKeyChecking=no -i ${SSH_KEY_PATH} ${EC2_USER}@${EC2_HOST} 'docker ps -a'
                    """
                }
            }
        }
        failure {
            script {
                echo "Build failed. Checking logs..."
                withCredentials([sshUserPrivateKey(credentialsId: params.SSH_CREDENTIALS_ID, keyFileVariable: 'SSH_KEY_PATH')]) {
                    sh """
                    ssh -o StrictHostKeyChecking=no -i ${SSH_KEY_PATH} ${EC2_USER}@${EC2_HOST} 'docker-compose logs'
                    """
                }
            }
        }
    }
}
