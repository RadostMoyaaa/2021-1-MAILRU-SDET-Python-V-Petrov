
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
             name: 'PYTEST_MARK'
        ) 
        string(
             defaultValue: "0",
             description: 'Threads number',
             name: 'THREADS_NUMBER'
        ) 
    }

    environment {
        PYTHON = "/usr/bin/python3.6"
        COMPOSE_NET = "docker_network_for_build_${BUILD_NUMBER}"
        MY_PROJECT_NAME = "test_myapp_with_jenkins" //TODO find builtin variable PROJECT_NAME
    }

    stages {

        stage("Build") {  // Preparing docker network, mock image

            steps {
 
                echo 'Creating docker compose network'
                sh "docker network inspect $COMPOSE_NET >/dev/null 2>&1 || docker network create $COMPOSE_NET"
                echo "Network $COMPOSE_NET created."
  
                echo 'Creating image of mock'
                sh '''
                    EXIST=$(docker image inspect mock:latest >/dev/null 2>&1 && echo 1 || echo 0)
                    if [[ "$EXIST" != 1 ]]; then
                        docker build -t mock:latest ./final-project/mock
                    fi
                '''
                echo 'Mock image created.'
            }
        }

        stage("Running tests") { 

            steps {

                script {

                        try {

                                withEnv(["PATH+EXTRA=$PYTHON","COMPOSE_NET=$COMPOSE_NET"]) {
                                            dir('final-project') {
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

        stage("Deleting Build Infrastructure") { //Turn off docker compose, removing all created containers, volumes, created test image
            
            steps {
                
                withEnv(["PATH+EXTRA=$PYTHON","COMPOSE_NET=$COMPOSE_NET"]) {
                    dir('final-project') {
                        sh "docker-compose down -v"
                        sh "docker-compose rm --force --stop  -v"
                        sh "docker ps -a | grep ${MY_PROJECT_NAME}_${BUILD_NUMBER} | awk '{print \$1}' | xargs docker rm"      //removing containers
                        sh "docker network rm $COMPOSE_NET"                                                     //removing network
                    }
                }
            }
        }


        stage('Generating reports') { // Generating allure report of current build passed tests 
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




