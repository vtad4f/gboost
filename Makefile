
all:
	mkdir build || true
	cd build ; cmake .. ; make
	
clean:
	rm -rf build