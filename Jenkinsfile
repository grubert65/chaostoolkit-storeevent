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

    stage('Make clean') {
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

    stage('Code linter') {
      steps {
        sh 'pip install pylama'
        sh 'pylama .'
      }
    }

    stage('Make test') {
      steps {
        sh 'make test'
      }
    }

    stage('Release') {
        when {
            branch 'master'
        }
        steps {
            withCredentials([usernamePassword(credentialsId:'Pypi_credentials', usernameVariable:'PYPI_USER_NAME', passwordVariable:'PYPI_PASSWORD')]) {
                sh 'make dist'
                sh 'make release'
            }
        }
    }

  }
}
