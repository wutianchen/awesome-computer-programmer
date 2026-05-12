# Setup EC2 instance

* install docker
* install minikube(k8s mini version)
etc


### Install docker on Amazon Linux

install docker compose

```bash
sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose version
```

### Install minikube

https://crishantha.medium.com/running-minikube-on-aws-ec2-e845337a956 (or https://www.linuxbuzz.com/how-to-install-minikube-on-fedora/)


```bash
# install minikube
# be careful to download the correct machine architecture
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# start minikube
minikube start

# vertify
minikube status

# open the minikube dashboard
# minikube dashboard
```

install k8s client kubectl (https://medium.com/@saeidlaalkaei/installing-kubectl-on-amazon-linux-2-machine-fc82a3e6b7c8)

```bash
# download
sudo curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo chmod +x kubectl
# move kubectl binary to a folder that is under system path
sudo mv kubectl /usr/local/bin/
# verify installation
kubectl version
```


### Install other tools related to k8s

* install krew on k8s (plugin manager of k8s) 

```bash
# follow this installation instruction https://krew.sigs.k8s.io/docs/user-guide/setup/install/
(
  set -x; cd "$(mktemp -d)" &&
  OS="$(uname | tr '[:upper:]' '[:lower:]')" &&
  ARCH="$(uname -m | sed -e 's/x86_64/amd64/' -e 's/\(arm\)\(64\)\?.*/\1\2/' -e 's/aarch64$/arm64/')" &&
  KREW="krew-${OS}_${ARCH}" &&
  curl -fsSLO "https://github.com/kubernetes-sigs/krew/releases/latest/download/${KREW}.tar.gz" &&
  tar zxvf "${KREW}.tar.gz" &&
  ./"${KREW}" install krew
)

# Add the $HOME/.krew/bin directory to your PATH environment variable.
export PATH="${KREW_ROOT:-$HOME/.krew}/bin:$PATH"

# refresh the shell
source ~/.bashrc

# verify installation

```

* install helm 

https://helm.sh/docs/intro/quickstart/

```bash
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
```