node('build-pod') {
    try {
        stage('checkout') {
            git branch: 'devel', url: 'https://github.com/ESGF/esgf-compute-cert'
        }
        
        stage('Setup build environment') {
            container('conda') {
                sh '''#!/bin/bash
                conda install -y -c conda-forge conda-build anaconda-client
                '''
            }
        }
        
        stage('Build package') {
            container('conda') {
                sh '''#!/bin/bash
                conda build -c conda-forge -c cdat conda/
                '''
            }
        }
        
        stage('Test install') {
            container('conda') {
                sh '''#!/bin/bash
                conda create -y -p ${HOME}/api \
                    -c conda-forge -c cdat \
                    esgf-compute-cert
                '''
                
                sh '''#!/bin/bash
                . /opt/conda/etc/profile.d/conda.sh

                conda activate ${HOME}/api
                
                cwt-cert --help
                '''
            }
        }
        
        stage('Test install from environment file') {
            container('conda') {
                sh '''#!/bin/bash
                conda env create -p ${HOME}/api-env \
                    -f environment.yml
                '''
                
                sh '''#!/bin/bash
                . /opt/conda/etc/profile.d/conda.sh

                conda activate ${HOME}/api-env
                
                cwt-cert --help
                '''
            }
        }
        
        stage('Upload anaconda') {
            withCredentials([usernamePassword(credentialsId: 'jasonb5-anaconda', passwordVariable: 'PASSWORD', usernameVariable: 'USERNAME')]) {
                container('conda') {
                    sh '''#!/bin/bash
                    anaconda login --username ${USERNAME} --password ${PASSWORD}
                    '''
                    
                    sh '''#!/bin/bash
                    anaconda upload --force -u cdat $(conda build --output conda/)
                    '''
                }
            }
        }
    } catch (e) {
        mail body: "Details ${BUILD_URL}", \
        subject: "Build ${BUILD_NUMBER} failed", \
        to: "boutte3@llnl.gov"
        
        throw e
    }
}
