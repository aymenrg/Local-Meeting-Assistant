import asyncio
import tempfile
import os
from src.agent_x.application.ports.interfaces import IScreenScanner

class WaylandScreenScanner(IScreenScanner):
    """Concrete implementation using Ubuntu native Wayland tools."""

    async def capture_visible_context(self) -> str:
        """Captures a screenshot with grim and extracts text with tesseract."""
        # Create a temporary file that is automatically deleted by the OS
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_img:
            img_path = temp_img.name

        try:
            # Step 1: Capture screen (runs grim as an async subprocess)
            capture_proc = await asyncio.create_subprocess_exec("grim", img_path)
            await capture_proc.communicate()

            if capture_proc.returncode != 0:
                raise RuntimeError("Wayland screen capture (grim) failed.")

            # Step 2: Extract text (runs tesseract as an async subprocess)
            ocr_proc = await asyncio.create_subprocess_exec(
                "tesseract", img_path, "stdout",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, _ = await ocr_proc.communicate()
            
            return stdout.decode('utf-8').strip()

        finally:
            # [PRIVACY RULE]: Always securely delete the image file from disk immediately
            if os.path.exists(img_path):
                os.remove(img_path)
