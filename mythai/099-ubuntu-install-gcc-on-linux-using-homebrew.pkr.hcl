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
  image        = "002-jolly-penguin"
  output_image = "099-install-gcc-on-linux-using-homebrew"
  container_name = "mythai"
  reuse        = true
  skip_publish = true
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
      "099-install-gcc-on-linux-using-homebrew.sh",
    ]
  }
}