import http.server
import socketserver
from argparse import ArgumentParser
from pathlib import Path
from typing import Any


def serve_project(serve_dir: Path, hostname: str, port: int) -> None:
    class CustomHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args: Any, **kwargs: Any) -> None:  # noqa: ANN401
            super().__init__(*args, directory=serve_dir, **kwargs)

    with socketserver.TCPServer((hostname, port), CustomHandler) as httpd:
        print(f"Serving at http://{hostname}:{port}")
        httpd.serve_forever()


if __name__ == "__main__":
    parser = ArgumentParser(description="serve the project")
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", "-p", type=int, default=8080)
    parser.add_argument("--dir", "-d", type=Path, default=Path(__file__).parents[2] / "public")
    args = parser.parse_args()

    exit(serve_project(args.dir, args.host, args.port))
