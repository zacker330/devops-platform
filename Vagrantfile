# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.

Vagrant.configure(2) do |config|


  ANSIBLE_RAW_SSH_ARGS = []
  VAGRANT_VM_PROVIDER = "virtualbox"
  machine_box = "CentOS-7.1.1503-x86_64-netboot"
  #machine_box = "https://github.com/2creatives/vagrant-centos/releases/download/v6.5.3/centos65-x86_64-20140116.box"

     config.vm.define "p1" do |machine|
       machine.vm.box = machine_box
       machine.vm.network "private_network", ip: "192.168.61.11"
       machine.vm.provider "virtualbox" do |node|
           node.name = "p1"
           node.memory = 3000
           node.cpus = 2
       end
      end



       config.vm.define "p2" do |machine|
         machine.vm.box = machine_box
         machine.vm.network "private_network", ip: "192.168.61.12"
         machine.vm.provider "virtualbox" do |node|
             node.name = "p2"
             node.memory = 2048
             node.cpus = 2
         end
        end

        config.vm.define "p3" do |machine|
          machine.vm.box = machine_box
          machine.vm.network "private_network", ip: "192.168.61.13"
          machine.vm.provider "virtualbox" do |node|
              node.name = "p3"
              node.memory = 4096
              node.cpus = 2
          end
         end

       config.vm.define "p4" do |machine|
         machine.vm.box = machine_box
         machine.vm.network "private_network", ip: "192.168.61.14"
         machine.vm.provider "virtualbox" do |node|
             node.name = "p4"
             node.memory = 2048
             node.cpus = 2
         end
        end

      config.vm.define "p5" do |machine|
        machine.vm.box = machine_box
        machine.vm.network "private_network", ip: "192.168.61.15"
        machine.vm.provider "virtualbox" do |node|
            node.name = "p5"
            node.memory = 2048
            node.cpus = 2
        end
       end
       config.vm.define "p6" do |machine|
         machine.vm.box = machine_box
         machine.vm.network "private_network", ip: "192.168.61.16"
         machine.vm.provider "virtualbox" do |node|
             node.name = "p6"
             node.memory = 2048
             node.cpus = 2
         end
        end
end
