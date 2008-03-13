install_path=/opt/nicos


all:
	@echo "targets: make install or make clean"

install: clean
	cp -a dconv $(install_path)/ui

clean:
	rm dconv/*.pyc
	rm dconv/*~
