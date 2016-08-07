Tools for building my Ducky-flavored LLVM version
=================================================

Usage
-----

.. code-block:: bash

  # clone happz/llvm-build repository
  git clone https://github.com/happz/llvm-build.git
  cd llvm-build
  # build image
  docker build -t ducky-llvm-builder .
  # run the image
  docker-compose up --force-recreate
  # wait for it...
  ls -alh /tmp/llvm-release.tar.gz

