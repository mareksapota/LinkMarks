#!/bin/bash

# Check this file into a project using PressUI.  You should put it in
# `MyProject/.get_pressui.sh`.

CUR=$PWD
DEST=${PWD}/PressUI

if [[ ! -e "$DEST" ]]; then
    echo 'Getting a fresh clone of PressUI'
    git clone 'https://github.com/maarons/pressui.git' "$DEST" || exit 1
else
    mount | grep "on $DEST type none" | grep 'bind' &> /dev/null
    IS_BIND_MOUNTED=$?
    # bind mounts and symlinks are used for testing and development
    if [[ $IS_BIND_MOUNTED -ne 0 && ! -L "$DEST" ]]; then
        echo 'Updating PressUI'
        cd "$DEST" &> /dev/null || exit 1
        git checkout master && git pull -f || exit 1
    else
        echo 'PressUI symlinked or bind mounted, not touching'
    fi
fi

# Update this script
diff "${DEST}/get_pressui.sh" "${CUR}/.get_pressui.sh" &> /dev/null
IS_DIFFERENT=$?

if [[ $IS_DIFFERENT -ne 0 ]]; then
    echo 'Getting new .get_pressui.sh and running it again'
    cp "${DEST}/get_pressui.sh" "${CUR}/.get_pressui.sh" || exit 1
    ${DEST}/get_pressui.sh || exit 1
fi
