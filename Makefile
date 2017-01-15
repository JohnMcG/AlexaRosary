install:
	./update.bash

test:
	$(MAKE) -C test test


.PHONY: test install
