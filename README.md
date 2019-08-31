
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![GPL License][license-shield]][license-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/ODEX-TOS/tos-installer-backend">
    <img src="https://tos.pbfp.xyz/images/logo.svg" alt="Logo" width="150" height="200">
  </a>

  <h3 align="center">Installer API</h3>
  <p align="center">
    An API for installing linux based Operating systems
    <br />
    <a href="https://github.com/ODEX-TOS/tos-installer-backend"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/ODEX-TOS/tos-installer-backend">View Demo</a>
    ·
    <a href="https://github.com/ODEX-TOS/tos-installer-backend/issues">Report Bug</a>
    ·
    <a href="https://github.com/ODEX-TOS/tos-installer-backend/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)



<!-- ABOUT THE PROJECT -->
## About The Project


<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

All you need for the installer to function is 
* python3
* python-argparser(should be included in python3)
* python-yaml


### Installation

1. Clone the tos-installer-backend
```sh
git clone https:://github.com/ODEX-TOS/tos-installer-backend.git
```
2. Install dependencies
* python3
* python-yaml
* python-argparser

3. supply a config file
```bash
python3 --in config.yaml # this will generate shell commands on stdout
python3 --in config.yaml --out install.sh # this will generate a shell file with all the commands
```

   

<!-- USAGE EXAMPLES -->
## Usage

> This explenation is a short version of everything you can do with this installer. If you want more information go to the wiki

Our installer works with yaml. If you are unfamiliar with yaml I suggest you look it up.
Our yaml file is divided into 2 sections called `models` and `execution`
The model defines how your installation will look like (eg your disk layout, software to be installed etc)
The execition is a sort of pipeline of steps the program will take during installation (eg first make the partitions then format them etc)
Here is the most basic configuration

```yaml
models:
- disks:
      - disk:
          device: "/dev/sda" # can also be /dev/disk/by-uuid or a command in the form $(command here)
          size: "499G"
          gpt: true # is the partitiontable gpt or msdos (by default gpt if not set)
          partitions:
            - partition:
                name: "efi" # just a usefull name to assign a partitions
                mount: "/boot/efi" # place to mount the partition
                filesystem: "fat32" # type of filesystem as defined in model.models.partition.EFilesystem
                start: "1MiB" # parted syntax for defining a location
                end: "200MiB"
execution:
  - partitiontable: "/dev/sda" # build a partition table
```

The above will build a partition table with one entry. It will put the partition table on `/dev/sda` and it will contain one partition with (boot partition)

Here is a short list of models you can define
* `disk` - a drive containing partitions and possibly logic volumes (by default UEFI no MBR)
* `chroot` - An environment to change root to (usefull to mimic a system)
* `user` - A user on the system
* `system` - General system specs (local, keymap, hostname etc)
* `script` - A custom script that can be executed
* `packages` - Software packages to be installed
* `network` - Setting to connect to a network


> Options and examples of these can be found in our [wiki](https://www.github.com/ODEX-TOS/tos-installer-backend/wiki

Now we also have the execution step. Think of it as a build process. It will execute steps from top to bottom

Here is a short list of build steps you can define
* `partitiontable` - Build a partition table based on a disk
* `format` - Format all partitions on a disk (or a single partition)
* `mount` - Mount all partitions on a disk (or a single partition)
* `network` - connect to a network if no connection exists yet
* `bootstrap` - Bootstrap the system to a mountpoint
* `fstab` - Build the fstab file
* `script` - Execute a script
* `chroot` - Change root to a mountpoint and execute steps there
* `systemsetup` - Configure the base system
* `createuser` - create a user
* `bootloader` - Install a bootloader to the boot partition (currently only supports grub, you could make a script to replace this step)
* `packages` - Install an array of packages

Here is an example of all options and settings

```yaml
models:
  - disks:
      - disk:
          device: "/dev/sda" # can also be /dev/disk/by-uuid or a command in the form $(command here)
          size: "499G"
          gpt: true # is the partitiontable gpt or msdos (by default gpt if not set)
          partitions:
            - partition:
                name: "efi" # just a usefull name to assign a partitions
                mount: "/boot/efi" # place to mount the partition
                filesystem: "fat32" # type of filesystem as defined in model.models.partition.EFilesystem
                start: "1MiB" # parted syntax for defining a location
                end: "200MiB"
            - partition:
                name: "swap"
                mount: "swap"
                filesystem: "ext4"
                start: "200MiB"
                end: "8GiB"
            - partition:
                name: "root"
                mount: "/"
                filesystem: "luks"
                start: "8GiB"
                end: "100%"
                encrypted: True
                logicvolumes:
                  - volume:
                      name: "root"
                      size: "200G"
                      mountpoint: "/"
                  - volume:
                      name: "home"
                      size: "200G"
                      mountpoint: "/home"
  - chroots:
      - chroot:
          name: "alpha" # name of the user to chroot
          mount: "/media" # alternative mountpoint to chroot to
      - chroot:
          name: "root"
  - users:
      - user:
          name: "alpha" # user by the name alpha
          password: "123" # the password of said user
      - user:
          name: "zetta"
          password: "456"
          shell: "/bin/zsh" # default shell for the user
          groups:
            - wheel
            - power
  - system:
      local: "en_US.UTF-8"
      keymap: "be-latin1"
      hostname: "tos"
      password: "123"
  - packages:
      - package:
          name: "userpackages"
          packagefile: "packages.txt" # either from a file
          package: # or a list in this format
            - a
            - b
  - scripts:
      # todo script should have a user an base command (/bin/sh)
      - script:
          name: "script1"
          file: "test.sh"
          command: "echo hello world"
      - script:
          name: "script2"
          file: "show.sh"
  - network:
      ssid: "ssid"
      password: "passphrase"
execution:
  - partitiontable: "/dev/sda" # build a partition table
  - format: "/dev/sda" # format a drive
  - format: "efi" # format partition based on its name
  - mount: "/dev/sda" # mount all partitions from this drive you can also specify a partition
  - network: # try to get a network connection if no connection already exists
  - bootstrap: # bootstrap the system
  - fstab: # generate fstab based on mounted partitions
  - chroot:
      user: "root" # execute the next steps in the chrooted environment
      steps:
        - systemsetup:
        - createuser: "alpha"
        - bootloader: "/dev/sda" # point to a disk model
  - chroot:
      user: "alpha"
      steps:
        - packages: "userpackages"
        - script: "script1"
  - script: "script1"
```


_For more examples, please refer to the [Documentation](https://www.github.com/ODEX-TOS/tos-installer-backend/wiki)_



<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/ODEX-TOS/tos-installer-backend/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the GPL License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

F0xedb - tom@odex.be

Project Link: [https://github.com/ODEX-TOS/tos-installer-backend](https://github.com/ODEX-TOS/tos-installer-backend)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* [ODEX-TOS](https://github.com/ODEX-TOS/tos-installer-backend)





<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/ODEX-TOS/tos-installer-backend.svg?style=flat-square
[contributors-url]: https://github.com/ODEX-TOS/tos-installer-backend/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/ODEX-TOS/tos-installer-backend.svg?style=flat-square
[forks-url]: https://github.com/ODEX-TOS/tos-installer-backend/network/members
[stars-shield]: https://img.shields.io/github/stars/ODEX-TOS/tos-installer-backend.svg?style=flat-square
[stars-url]: https://github.com/ODEX-TOS/tos-installer-backend/stargazers
[issues-shield]: https://img.shields.io/github/issues/ODEX-TOS/tos-installer-backend.svg?style=flat-square
[issues-url]: https://github.com/ODEX-TOS/tos-installer-backend/issues
[license-shield]: https://img.shields.io/github/license/ODEX-TOS/tos-installer-backend.svg?style=flat-square
[license-url]: https://github.com/ODEX-TOS/tos-installer-backend/blob/master/LICENSE.txt
[product-screenshot]: https://tos.pbfp.xyz/images/logo.svg
