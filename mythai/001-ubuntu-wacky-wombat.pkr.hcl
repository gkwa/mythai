packer {
  required_plugins {
    incus = {
      version = ">= 1.0.0"
      source  = "github.com/bketelsen/incus"
    }
    ansible = {
      version = "~> 1"
      source = "github.com/hashicorp/ansible"
    }
  }
}

source "incus" "jammy" {
  image        = "images:ubuntu/focal"
  output_image = "001-wacky-wombat"
  container_name = "mythai"
  reuse        = true
  skip_publish = false
}

build {
  sources = ["incus.jammy"]

  provisioner "shell" {
    inline = [
      "cloud-init status --wait",
    ]
  }

  provisioner "shell" {
    scripts = [
      "001-wacky-wombat.sh",
    ]
  }
}
