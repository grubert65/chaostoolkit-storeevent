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

    stage('make clean') {
      steps {
        sh 'make clean'
      }
    }

    stage('Code formatter') {
      steps {
        sh 'pip install autopep8'
        sh 'autopep8 --in-place --aggressive --aggressive *.py'
        sh 'autopep8 --in-place --aggressive --aggressive chaosdb/*.py'
        sh 'autopep8 --in-place --aggressive --aggressive tests/*.py'
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
