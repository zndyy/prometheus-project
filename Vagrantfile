Vagrant.configure("2") do |config|
  config.vm.box = "bento/rockylinux-9"

  config.vm.network "private_network", ip: "192.168.56.10"
  config.vm.synced_folder ".", "/vagrant", disabled: true
end
