
all:
	mkdir build || true
	cd build ; cmake .. ; make
	cd src-main/conversion ; ./convert.sh
   
clean:
	rm -rf build