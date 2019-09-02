pipeline {
  agent {
    docker {
      image 'python:3.7'
    }
  }
  stages {

    stage('Install requirements') {
      steps {
        sh 'pip install -U pip'
        sh 'pip install -r requirements-dev.txt'
        sh 'pip install -r requirements.txt'
      }
    }

    stage('Linter') {
      steps {
        sh 'pip install pylama'
        sh 'pylama .'
      }
    }

  }
}
