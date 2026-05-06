#!/bin/bash

set -e

echo "Instalando xcb-util-keysyms en local..."

#Ir a una carpeta temporal
cd /tmp

#Descargar si no existe
if [ ! -d "xcb-util-keysyms-0.4.0" ]; then
    wget https://xcb.freedesktop.org/dist/xcb-util-keysyms-0.4.0.tar.gz
    tar -xzf xcb-util-keysyms-0.4.0.tar.gz
fi

cd xcb-util-keysyms-0.4.0

#Compilar e instalar en ~/.local
./configure --prefix=$HOME/.local
make -j$(nproc)
make install

echo "Librería instalada en ~/.local"

#Exportar variables
export CFLAGS="-I$HOME/.local/include"
export LDFLAGS="-L$HOME/.local/lib"
export LD_LIBRARY_PATH="$HOME/.local/lib:$LD_LIBRARY_PATH"

echo " Compilando MLX..."

#Cambia esta ruta si tu MLX está en otro sitio
cd ~/sgoinfre/amaze/mlx_CLXV

make clean
make

echo "MLX compilada correctamente"
echo "Recuerda exportar LD_LIBRARY_PATH si abres otra terminal"
