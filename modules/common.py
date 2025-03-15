import fal_client
from rich.console import Console

cl = Console()


def uploadFile(filePath: str) -> str:
    cl.print("\n\n==============================================")
    cl.print("Uploading file...")
    cl.print(f"file_path: [yellow]{filePath}[/yellow]")
    cl.print("==============================================\n\n")
    returnURL: str = fal_client.upload_file(path=filePath)
    cl.print(f"Return URL: {returnURL}")
    return returnURL
