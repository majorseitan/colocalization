all: static

ui/package-lock.json:
	(cd ui; yes | npm install )
static:
	(cd ui; rm -rf ../static; npm run build && cp -R build ../static)
