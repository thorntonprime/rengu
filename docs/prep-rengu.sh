#!/bin/sh

dnf install -y \
  python3-textblob python3-blitzdb python3-nltk python3-enchant python3-xapian \
  yamllint jq msort
groupadd -g 400 rengu
useradd -u 400 -g 400 -d /srv/rengu rengu


