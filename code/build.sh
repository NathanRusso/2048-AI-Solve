#!/bin/bash

gcc -c expectiminimax.c  
gcc -o expectiminimax expectiminimax.o
gcc -shared -o expectiminimax.dll expectiminimax.o
