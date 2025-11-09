pipeline {
  agent any
  environment {
    DOCKERHUB_REPO = '2024ht66001/aceest-fitness'
    APP_NAME = 'aceest-fitness'
  }
  stages {
    stage('Checkout') {
      steps { checkout scm }
    }
    stage('Install deps & Test') {
      steps {
        sh 'python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt pytest'
        sh '. .venv/bin/activate && pytest'
      }
    }
    stage('Sonar Quality') {
      when { expression { return env.SONAR_TOKEN != null } }
      steps {
        sh '''
          curl -sL https://sonarcloud.io/static/cpp/build-wrapper-linux-x86.zip >/dev/null || true
          # Minimal: use scanner-cli via Docker (simpler):
          docker run --rm -e SONAR_HOST_URL=$SONAR_HOST_URL -e SONAR_TOKEN=$SONAR_TOKEN \
            -v $PWD:/usr/src sonarsource/sonar-scanner-cli
        '''
      }
    }
    stage('Build Docker Image') {
      steps {
        script {
          def tag = sh(script: "git describe --tags --abbrev=0 || echo v0.0.0", returnStdout: true).trim()
          sh "docker build -t ${DOCKERHUB_REPO}:${tag} ."
        }
      }
    }
    stage('Push Image') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'admin', passwordVariable: '2d06d7b084b7431d9bb0df0e37c0aa30')]) {
          sh 'echo $PASS | docker login -u $USER --password-stdin'
          def tag = sh(script: "git describe --tags --abbrev=0 || echo v0.0.0", returnStdout: true).trim()
          sh "docker push ${DOCKERHUB_REPO}:${tag}"
        }
      }
    }
    stage('Deploy to Kubernetes') {
      steps {
        sh '''
          kubectl cluster-info
          kubectl apply -f k8s/namespace.yaml
          kubectl apply -f k8s/deployment-blue.yaml
          kubectl apply -f k8s/service.yaml
        '''
      }
    }
  }
}
