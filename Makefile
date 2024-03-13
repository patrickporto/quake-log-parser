build:
	@docker build -t quakelogparser .

run: build
	@docker run -it --rm quakelogparser \
		parser-cli source add-url https://gist.githubusercontent.com/cloudwalk-tests/be1b636e58abff14088c8b5309f575d8/raw/df6ef4a9c0b326ce3760233ef24ae8bfa8e33940/qgames.log && \
		poetry run parser-cli ingestion pull && \
		poetry run parser-cli ingestion run && \
		poetry run parser-cli player-ranking
