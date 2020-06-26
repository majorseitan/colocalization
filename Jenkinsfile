pipeline {
    agent any

    environment {
        PYTHONPATH = '.'
    }

    stages {
        stage('build') {
            steps { sh 'pip3 install -r requirements.txt'
		    sh 'coverage run -m pytest'
		    sh 'pylint scripts > pylint.log || exit 0'
		    sh 'safety check -r requirements/docker.txt'
		    sh 'safety check'
		    sh 'pyflakes scripts'
		    sh 'mypy scripts'
		    sh 'prospector'
		    sh 'bandit -r scripts'
		    sh 'docker build -t majorseitan/colocalization:latest -f Dockerfile'
            }
        }
    }
}