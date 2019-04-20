
all:
	mkdir -p build
	cd build ; cmake .. ; make
	cd src-main/conversion ; ./convert.sh
   
clean:
	rm -rf build