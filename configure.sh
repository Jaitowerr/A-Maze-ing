#!/bin/sh

echo "Checking system configuration for your library..."
echo

DEPS_OK=1
MISSING=""


CC=${CC:-cc}


check_header() {
    HEADER="$1"
    PKG="$2"

    echo -n "Checking for header <$HEADER>... "

    echo "#include <$HEADER>" | \
        $CC -I$HOME/.local/include $CFLAGS -E - >/dev/null 2>&1

    if [ $? -eq 0 ]; then
        echo "found"
    else
        echo "not found"
        DEPS_OK=0
        MISSING="$MISSING\n  - include: <$HEADER>\t=> $PKG"
    fi
}

check_lib() {
    LIBNAME="$1"
    PKG="$2"

    echo -n "Checking for library -l$LIBNAME... "

    echo "int main(){return 0;}" | \
        $CC -L$HOME/.local/lib $CFLAGS $LDFLAGS -x c - -l$LIBNAME >/dev/null 2>&1

    if [ $? -eq 0 ]; then
        echo "found"
    else
        echo "not found"
        DEPS_OK=0
        MISSING="$MISSING\n  - library: -l$LIBNAME\t=> $PKG"
    fi
}

check_header "vulkan/vulkan.h" "vulkan-headers"
check_lib "vulkan" "vulkan-loader"

check_header "xcb/xcb.h" "libxcb"
check_lib "xcb" "libxcb"

check_header "xcb/xcb_keysyms.h" "xcb-util-keysyms"
check_lib "xcb-keysyms" "xcb-util-keysyms"

check_header "vulkan/vulkan_xcb.h" "vulkan-headers"

check_header "zlib.h" "zlib"
check_lib "z" "zlib"

check_header "bsd/bsd.h" "libbsd"
check_lib "bsd" "libbsd"

rm -f a.out

echo
if [ $DEPS_OK -eq 1 ]; then
    echo " All required headers and libraries are available."
    exit 0
else
    echo " Some dependencies are missing or not accessible:"
    echo -e "$MISSING"
    echo
    echo "Try:"
    echo "  export CFLAGS='-I$HOME/.local/include'"
    echo "  export LDFLAGS='-L$HOME/.local/lib'"
    exit 1
fi