provider "null" {}

resource "null_resource" "vagrant_up" {
  provisioner "local-exec" {
    command     = "vagrant up"
    working_dir = "${path.module}"
  }
}

resource "null_resource" "disable_firewalld" {
  depends_on = [null_resource.vagrant_up]

  connection {
    type        = "ssh"
    host        = "192.168.56.10"
    user        = "vagrant"
    password    = "vagrant" 
    timeout     = "30s"
  }

  provisioner "remote-exec" {
    inline = [
      "sudo firewall-cmd --zone=public --add-port=8080/tcp --permanent",
      "sudo firewall-cmd --reload"
    ]
  }
}

resource "null_resource" "ansible_playbook" {
  depends_on = [null_resource.disable_firewalld]

  provisioner "local-exec" {
    command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i ./ansible/inventory ./ansible/deploy.yml -e deploy_method=docker"
  }
}
