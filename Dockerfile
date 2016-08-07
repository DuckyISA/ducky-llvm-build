FROM ubuntu:trusty

MAINTAINER Milos Prchlik <happz@happz.cz>

RUN apt-get update && apt-get install -y build-essential lsb-release git make ninja-build wget
RUN mkdir -p /llvm-build
ADD Makefile /llvm-build/Makefile
