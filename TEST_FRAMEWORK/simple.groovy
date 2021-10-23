
pipeline {

    agent {
        label 'master' //All build would be created on Jenkins host machine
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '5')) // Number of old builds saved
        timestamps()
    }

    parameters { 
        string(
             defaultValue: "api or ui",
             description: 'Pytest marks tests parameter',
             name: 'MARK'
        ) 
        string(
             defaultValue: "0",
             description: 'Workers number',
             name: 'WORKERS'
        ) 
    }

    environment {
        PYTHON = "/usr/bin/python3.6"
        COMPOSE_NET = "docker_network_for_build_${BUILD_NUMBER}"
        MY_PROJECT_NAME = "test_myapp_with_jenkins"
    }

    stages {

        stage("Preparing docker network") {

            steps {
 
                echo 'Creating docker compose network'
                sh "docker network inspect $COMPOSE_NET >/dev/null 2>&1 || docker network create $COMPOSE_NET"
                echo "Network $COMPOSE_NET created."
            }
        }

        stage("Executing tests") {

            steps {

                script {

                        try {

                                withEnv(["PATH+EXTRA=$PYTHON","COMPOSE_NET=$COMPOSE_NET"]) {
                                            dir('TEST_FRAMEWORK/final-project') {
                                                sh "docker-compose --project-name ${MY_PROJECT_NAME}_${BUILD_NUMBER}  up --exit-code-from selenoid"
                                            }
                                }

                        } catch(Exception e) {
                            error "Stage interrupted with ${e.toString()}"
                            sh "exit 1"
                        }            
                }                
            }
        }

        stage("Closing and deleting infrastructure") { // Turn off docker compose, removing all created containers, volumes, created test image
            
            steps {
                
                withEnv(["PATH+EXTRA=$PYTHON","COMPOSE_NET=$COMPOSE_NET"]) {
                    dir('TEST_FRAMEWORK/final-project') {
                        sh "docker-compose down -v"
                        sh "docker-compose rm --force --stop  -v"
                        sh "docker ps -a | grep ${MY_PROJECT_NAME}_${BUILD_NUMBER} | awk '{print \$1}' | xargs docker rm"
                        sh "docker network rm $COMPOSE_NET"
                    }
                }
            }
        }


        stage('Generating reports') { // Allure
            steps {
                script {
                        allure([
                                reportBuildPolicy: 'ALWAYS',
                                results: [[path: '$WORKSPACE/allure-results']]
                        ])
                }
            }
        }
    }

   post { //Cleaning working directory 

        always { 

                echo "POST STAGE"
                cleanWs()
        }
    }
}




