import sys
import threading
import time
from queue import Queue

from ..db.models import DatabaseManager
from ..speech.tts_manager import TTSManager


class BarcodeInputHandler:
    """
    Handles barcode scanner input from the terminal.
    Runs in a separate thread to avoid blocking the main OCR functionality.
    """

    def __init__(self, db_manager=None, tts_manager=None):
        self.db_manager = db_manager or DatabaseManager()
        self.tts_manager = tts_manager or TTSManager()
        self.input_thread = None
        self.running = False
        self.input_queue = Queue()
        self.current_barcode = ""

    def start(self):
        """Start the barcode input handler thread"""
        if self.input_thread and self.input_thread.is_alive():
            return

        self.running = True
        self.input_thread = threading.Thread(target=self._input_loop, daemon=True)
        self.input_thread.start()
        print("Barcode input handler started - ready to scan barcodes")

    def stop(self):
        """Stop the barcode input handler thread"""
        self.running = False
        if self.input_thread and self.input_thread.is_alive():
            self.input_thread.join(timeout=1.0)

    def _input_loop(self):
        """Main input loop that runs in a separate thread"""
        # Start a separate thread to read from stdin
        input_reader = threading.Thread(target=self._read_input, daemon=True)
        input_reader.start()

        while self.running:
            # Process any barcodes in the queue
            try:
                if not self.input_queue.empty():
                    barcode = self.input_queue.get(block=False)
                    self._process_barcode(barcode)
                time.sleep(0.1)  # Sleep to reduce CPU usage
            except Exception as e:
                print(f"Error in barcode input processing: {e}")

    def _read_input(self):
        """Read input from stdin and place it in the queue"""
        while self.running:
            try:
                # This will block waiting for input, but it's in its own thread
                barcode = input().strip()
                if barcode:
                    self.input_queue.put(barcode)
            except EOFError:
                # Handle EOF (Ctrl+D)
                time.sleep(0.5)
                continue
            except Exception as e:
                print(f"Error reading barcode input: {e}")
                time.sleep(0.5)

    def _process_barcode(self, barcode):
        """Process a scanned barcode"""
        print(f"\nBarcode scanned: {barcode}")

        # Look up the barcode in the database
        barcode_info = self.db_manager.get_barcode(barcode)

        if barcode_info:
            message = (
                f"Product: {barcode_info.product_name}, Brand: {barcode_info.brand}"
            )
            print(message)

            # Speak the product information if TTS is available
            if self.tts_manager:
                self.tts_manager.say_async(message)
        else:
            message = f"Unknown barcode: {barcode}"
            print(message)

            # Speak the error message if TTS is available
            if self.tts_manager:
                self.tts_manager.say_async("Unknown barcode scanned")
