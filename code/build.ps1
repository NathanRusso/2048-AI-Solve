gcc -c expectiminimax.c  
gcc -o expectiminimax expectiminimax.o
gcc -shared -o expectiminimax.dll expectiminimax.o
gcc -c expectiminimax_int.c  
gcc -o expectiminimax_int expectiminimax_int.o
gcc -shared -o expectiminimax_int.dll expectiminimax_int.o
