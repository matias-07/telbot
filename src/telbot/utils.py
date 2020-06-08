def is_photo(content):
	return len(content.split()) == 1 and any(map(
		lambda e: content.endswith(f".{e}"),
		["jpg", "png", "gif", "jpeg"]
	))
