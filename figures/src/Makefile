# Regenerate all programmatic figures. Each figure is a script; the shared
# stylesheet lives in lqftbook.mplstyle. Outputs land in figures/.
PY = python3
SCRIPTS := $(wildcard fig*.py)
TARGETS := $(SCRIPTS:.py=.done)

all: $(TARGETS)

%.done: %.py lqftbook.mplstyle
	$(PY) $<
	touch $@

clean:
	rm -f *.done
