def is_photo(content):
	return len(content.split()) == 1 and any(map(
		lambda e: content.endswith(f".{e}"),
		["jpg", "png", "jpeg"]
	))

def is_animation(content):
	return len(content.split()) == 1 and content.endswith(".gif")
