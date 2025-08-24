"""
Barcode Input Handler for the Vision-Impaired Shopping Assistant.

This module provides real-time barcode scanning capabilities through terminal input,
running in a separate thread to avoid blocking the main application. It integrates
with the database system to lookup product information and uses text-to-speech
to provide audio feedback about scanned products.

The handler supports:
- Threaded barcode input to prevent blocking the camera/OCR system
- Database lookup for product information including allergen data
- Text-to-speech announcements for product details
- Graceful error handling and recovery
- Queue-based input processing for reliability

Usage:
    handler = BarcodeInputHandler(db_manager, tts_manager)
    handler.start()  # Begin scanning for barcode input
    # ... main application continues running ...
    handler.stop()   # Clean shutdown when done
"""

import sys
import threading
import time
from queue import Queue

from ..config import Config
from ..db.models import DatabaseManager
from ..speech.tts_manager import TTSManager


class BarcodeInputHandler:
    """
    Handles barcode scanner input from the terminal.
    Runs in a separate thread to avoid blocking the main OCR functionality.
    """

    def __init__(self, db_manager=None, tts_manager=None):
        """
        Initialize the barcode input handler with optional dependencies.

        Args:
            db_manager (DatabaseManager, optional): Database manager for barcode lookups.
                                                   If None, creates a new instance.
            tts_manager (TTSManager, optional): Text-to-speech manager for audio feedback.
                                              If None, creates a new instance.
        """
        self.db_manager = db_manager or DatabaseManager()
        self.tts_manager = tts_manager or TTSManager()
        self.input_thread = None
        self.running = False
        self.input_queue = Queue()
        self.current_barcode = ""

    def start(self):
        """
        Start the barcode input handler in a background thread.

        Creates a daemon thread that listens for barcode input and processes
        it asynchronously. If a thread is already running, this method returns
        without creating a new thread.
        """
        if self.input_thread and self.input_thread.is_alive():
            return

        self.running = True
        self.input_thread = threading.Thread(target=self._input_loop, daemon=True)
        self.input_thread.start()
        print("Barcode input handler started - ready to scan barcodes")

    def stop(self):
        """
        Stop the barcode input handler and wait for thread termination.

        Sets the running flag to False and waits up to 1 second for the
        input thread to terminate gracefully. Used for clean shutdown.
        """
        self.running = False
        if self.input_thread and self.input_thread.is_alive():
            self.input_thread.join(timeout=1.0)

    def _input_loop(self):
        """
        Main processing loop that runs in the background thread.

        Starts a separate input reader thread and continuously processes
        barcodes from the queue. Uses a short sleep interval to reduce
        CPU usage while maintaining responsiveness.
        """
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
        """
        Read barcode input from stdin and queue it for processing.

        Runs in its own thread to avoid blocking other operations.
        Handles EOF conditions (Ctrl+D) and other input errors gracefully.
        Only non-empty barcodes are queued for processing.
        """
        while self.running:
            try:
                # This will block waiting for input, but it's in its own thread
                barcode = input().strip()
                if barcode:
                    self.input_queue.put(barcode)
            except EOFError:
                # Handle EOF (Ctrl+D) gracefully
                time.sleep(0.5)
                continue
            except Exception as e:
                print(f"Error reading barcode input: {e}")
                time.sleep(0.5)

    def _process_barcode(self, barcode):
        """
        Process a scanned barcode by looking it up and providing feedback.

        Performs database lookup for the barcode and provides both visual
        and audio feedback about the product. If found, announces product
        name, brand, and allergen information. If not found, announces
        that the barcode is unknown.

        Args:
            barcode (str): The scanned barcode identifier to process
        """
        print(f"\nBarcode scanned: {barcode}")

        # Look up the barcode in the database
        barcode_info = self.db_manager.get_barcode(barcode)

        if barcode_info:
            # Format the TTS message with product information
            message = Config.TTS_BARCODE_FOUND_TEMPLATE.format(
                product_name=barcode_info.product_name,
                brand=barcode_info.brand,
                allergies=barcode_info.allergies or "none",
            )
            print(
                f"Product: {barcode_info.product_name}, Brand: {barcode_info.brand}, Allergies: {barcode_info.allergies or 'none'}"
            )

            # Provide audio feedback if TTS is available
            if self.tts_manager:
                self.tts_manager.say_async(message)
        else:
            # Handle unknown barcode case
            message = Config.TTS_BARCODE_NOT_FOUND_TEMPLATE.format(barcode=barcode)
            print(f"Unknown barcode: {barcode}")

            # Provide audio feedback for unknown barcode
            if self.tts_manager:
                self.tts_manager.say_async(message)
