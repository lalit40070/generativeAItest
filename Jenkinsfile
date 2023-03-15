pipeline{
    agent any
   
    stages{  
        stage('ECR Login'){
            steps{
                sh 'aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 858280339305.dkr.ecr.us-east-2.amazonaws.com'
            }
        }
        stage('Build Image'){
            steps{
                sh 'docker build -t generativeaitest:${BUILD_NUMBER} .'
            }
        }
        stage('Image Tag'){
            steps{
                sh 'docker tag generativeaitest:${BUILD_NUMBER} 858280339305.dkr.ecr.us-east-2.amazonaws.com/generativeaitest:${BUILD_NUMBER}'
            }
        }
        stage('Docker push'){
            steps{
                sh 'docker push 858280339305.dkr.ecr.us-east-2.amazonaws.com/generativeaitest:${BUILD_NUMBER}'
            }
        }
    }
