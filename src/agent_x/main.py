import sys
from PyQt6.QtWidgets import QApplication
from src.agent_x.domain.session_memory import SessionMemory
from src.agent_x.presentation.ui_overlay import PyQtPresenter
from src.agent_x.presentation.audio_worker import ContinuousAudioWorker

def main():
    app = QApplication(sys.argv)
    
    # 1. Initialize Domain Layer (The Brain)
    memory = SessionMemory(max_token_limit=3000)
    
    # 2. Initialize Presentation/UI Layer
    ui_overlay = PyQtPresenter()
    ui_overlay.show()
    
    # 3. Start the Background Audio Pipeline
    audio_worker = ContinuousAudioWorker(memory)
    audio_worker.start()
    
    # 4. Handle graceful shutdown and Privacy Purge
    def on_exit():
        audio_worker.is_running = False
        memory.purge()
        print("Application closed. RAM purged securely.")
        
    app.aboutToQuit.connect(on_exit)
    
    # Run the UI loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
