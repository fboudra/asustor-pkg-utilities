#!/bin/sh
# extract-admimage - Extract kernel/initramfs/rootfs from ADM 2.5-2.6 image
#
# (C) 2016 Fathi Boudra <fboudra@gmail.com>
# Licensed under the GNU General Public License, version 2 (GPLv2)

set -e

progname=$(basename $0)
imgfile=

usage() {
  printf "usage: ${progname} <adm-image>\n"
  exit 1
}

imgfile="$1"
[ -n "${imgfile}" ] || usage

imgheader=$(mktemp /tmp/adm-image-header.XXXXXX)
trap "rm -f ${imgheader}" 0
head -n 14 ${imgfile} | tail -n -12 > ${imgheader}
printf "Asustor ADM image header (${imgfile}) content:\n\n"
cat ${imgheader}
printf "\n"

[ -d ${imgfile}.out ] || mkdir ${imgfile}.out
tail -n +20 ${imgfile} > ${imgfile}.out/${imgfile}.tar
tar -xf ${imgfile}.out/${imgfile}.tar -C ${imgfile}.out

printf "Asustor ADM image extracted to ${imgfile}.out\n"
