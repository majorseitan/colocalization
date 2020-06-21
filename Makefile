static:
	(cd ui; rm -rf ../static; npm run build && cp -R build ../static)
