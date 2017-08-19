#!/usr/bin/env bash

# Replace all "c." with "constants."
# sed -i "s/c\./constants\./g" *.py
#
# Replace all " as c" with ""
# sed -i "s/ as c//g" *.py


rename() {
    sed -i "s/\"up\"/\"move_up\"/g" *.py
    sed -i "s/\"down\"/\"move_down\"/g" *.py
    sed -i "s/\"left\"/\"move_left\"/g" *.py
    sed -i "s/\"right\"/\"move_right\"/g" *.py
    sed -i "s/\"one\"/\"cut\"/g" *.py
    sed -i "s/\"two\"/\"tree\"/g" *.py
    sed -i "s/\"three\"/\"search\"/g" *.py
    sed -i "s/\"four\"/\"flip\"/g" *.py
}

cd ../src/components && rename
cd ../states && rename
