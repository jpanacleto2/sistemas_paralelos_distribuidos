#!/bin/bash

VM_NAME="vm1"
ISO_PATH="/var/lib/libvirt/boot/alpine-standard-3.19.1-x86_64.iso"
DISK_PATH="/var/lib/libvirt/images/${VM_NAME}.qcow2"
DISK_SIZE="10G"
MEMORY="512"
VCPUS="1"
NETWORK_NAME="vlan-vegenere"
MAC_ADDRESS="52:54:00:00:00:11"

# Verifica se o serviço libvirtd está ativo
if ! systemctl is-active --quiet libvirtd; then
    echo "O serviço libvirtd não está ativo. Iniciando..."
    sudo systemctl start libvirtd
fi

# Verifica se a ISO já foi baixada
if [ ! -f "$ISO_PATH" ]; then
    echo "Baixando a imagem do Alpine..."
    wget https://dl-cdn.alpinelinux.org/alpine/v3.19/releases/x86_64/alpine-standard-3.19.1-x86_64.iso -O /tmp/alpine.iso
    sudo mv /tmp/alpine.iso "$ISO_PATH"
else
    echo "Imagem do Alpine já existe em $ISO_PATH. Pulando download."
fi

# Criar a rede virtual se necessário
if ! virsh net-info "$NETWORK_NAME" &>/dev/null; then
    echo "Criando a rede virtual $NETWORK_NAME..."
    virsh net-create vlan-vegenere.xml
    virsh net-start "$NETWORK_NAME"
else
    echo "Rede $NETWORK_NAME já existe."
fi

# Criar o disco virtual
echo "Criando o disco virtual..."
sudo qemu-img create -f qcow2 "$DISK_PATH" "$DISK_SIZE"

# Criar a máquina virtual
echo "Criando a máquina virtual com rede VLAN e MAC fixo..."
sudo virt-install \
  --name "$VM_NAME" \
  --memory "$MEMORY" \
  --vcpus "$VCPUS" \
  --disk path="$DISK_PATH",format=qcow2 \
  --cdrom "$ISO_PATH" \
  --os-variant generic \
  --network network=$NETWORK_NAME,mac=$MAC_ADDRESS \
  --graphics none \
  --console pty,target_type=serial \
  --noautoconsole

# Rodar setup-alpine via expect
echo "Acessando a VM e executando o setup-alpine..."
sleep 5
expect setup-alpine.expect "$VM_NAME"

# Mensagem final
echo "A VM foi criada e o SSH foi configurado."
echo "Você pode acessar a VM agora via SSH usando o IP: $IP_ADDR"
echo "Comando: ssh root@$IP_ADDR"
