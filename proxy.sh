voms-proxy-init -voms cms -out $HOME/.globus/gridproxy.cert
export X509_USER_PROXY=${HOME}/.globus/gridproxy.cert
