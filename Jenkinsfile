pipeline {
  agent {
    docker {
      image 'python:3.7'
    }

  }
  stages {
    stage('Install requirements') {
      steps {
        sh '''pip install -r requirements-dev.txt
pip install -r requirements.txt'''
      }
    }
  }
}