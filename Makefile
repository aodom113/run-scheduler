docs:
	sphinx-build source public --fail-on-warning
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +