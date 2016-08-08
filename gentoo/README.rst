Docker image for building Ducky-flavored LLVM version
=====================================================


Gentoo
------


Usage
-----

.. code-block:: bash

  # clone happz/llvm-build repository
  git clone https://github.com/happz/llvm-build.git
  cd llvm-build/gentoo

  # either build the image...
  docker build -t ducky-llvm-builder-gentoo .

  # or pull it from Docker hub
  docker pull happz/ducky-llvm-builder-gentoo

  # run the image
  docker-compose up --force-recreate
  # wait for it...
  ls -alh /tmp/llvm-release.tar.gz
