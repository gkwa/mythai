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

source "incus" "base" {
  image        = "001-wacky-wombat"
  output_image = "002-jolly-penguin"
  container_name = "mythai"
  reuse        = true
  skip_publish = false
}

build {
  sources = ["incus.base"]

  provisioner "shell" {
    inline = [
      "cloud-init status --wait",
    ]
  }

  provisioner "shell" {
    scripts = [
      "002-jolly-penguin.sh",
    ]
  }
}