PKG_SCHEMA=package.schema.yaml
PKG_BUILD=python scripts/buildpkg.py

BUILD_DIR=build
OUTPUT_DIR=dist

CONVERT_SCRIPT=python scripts/dumpdb.py
OUTPUT_FORMATS=yaml json toml


COMMIT_SHA=$(shell git rev-parse HEAD)
NUMBER_SEQ=$(shell git rev-list --count HEAD)

DBPARTS=$(patsubst packages/%.yaml,${BUILD_DIR}/%.dbp,$(wildcard packages/*.yaml))
OUTPUT_FILES=$(patsubst %,${OUTPUT_DIR}/unipkg.%,$(OUTPUT_FORMATS))

all: ${BUILD_DIR}/ ${OUTPUT_DIR}/ ${OUTPUT_FILES}
clean: 
	rm -rf ${OUTPUT_DIR}/ ${BUILD_DIR}/

${BUILD_DIR}/%.pkg: packages/%.yaml
	${PKG_BUILD} ${PKG_SCHEMA} $^ > $@

${BUILD_DIR}/%.dbp: ${BUILD_DIR}/%.pkg
	sed -e '1!s/^/ /' $^ > $@

${BUILD_DIR}/:
	mkdir ${BUILD_DIR}/

${OUTPUT_DIR}/:
	mkdir ${OUTPUT_DIR}/

${OUTPUT_DIR}/unipkg.db: $(DBPARTS)
	echo "UNIPKG 1 $(COMMIT_SHA) $(NUMBER_SEQ)" > $@
	cat $^ >> $@

${OUTPUT_DIR}/unipkg.%: ${OUTPUT_DIR}/unipkg.db
	${CONVERT_SCRIPT} $^ $* > $@
