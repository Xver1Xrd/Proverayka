# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import (
    QPushButton,
    QWidget,
    QHBoxLayout,
)
from PyQt6.QtCore import QUrl, Qt, QTime
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtWidgets import (
    QLineEdit,
    QSlider,
    QDial,
    QPushButton,
    QWidget,
    QHBoxLayout

)

class Player(QWidget):                                          # видеоплеер
    def __init__(self, contentType, **kwargs):
        # stageType, file_path):                                # выбор файла
        super().__init__()

        self.mediaPlayer = QMediaPlayer()
        self.audioOutput = QAudioOutput()

        self.stageType = kwargs.get('stageType', None)
        self.file_path = kwargs.get('file_path', None)
        self.contentType = contentType
        # self.audioOutput.setVolume(50)
        self.mediaPlayer.setAudioOutput(self.audioOutput)

        if self.contentType == "video":
            self.videoWidget = QVideoWidget(self)
            self.mediaPlayer.setVideoOutput(self.videoWidget)

        self.mediaPlayer.playbackStateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.errorChanged.connect(self.handleError)
        self.playButton = QPushButton("▶️", self)
        self.playButton.setEnabled(False)
        self.playButton.resize(self.playButton.sizeHint())
        self.playButton.clicked.connect(self.play)
        self.pauseButton = QPushButton("⏸️", self)
        self.pauseButton.setEnabled(False)
        self.pauseButton.resize(self.pauseButton.sizeHint())
        self.pauseButton.clicked.connect(self.mediaPlayer.pause)
        self.stopButton = QPushButton("⏹️", self)
        self.stopButton.setEnabled(False)
        self.stopButton.resize(self.stopButton.sizeHint())
        self.stopButton.clicked.connect(self.stop)

        if self.file_path != None:
            self.mediaPlayer.setSource(QUrl.fromLocalFile(self.file_path))
            self.playButton.setEnabled(True)

        self.volumeSlider = QDial(self)
        self.volumeSlider.valueChanged.connect(
            self.setVolume)
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.setSingleStep(1)
        self.volumeSlider.setPageStep(20)
        self.volumeSlider.setValue(20)
        self.controlLayout = QHBoxLayout()
        self.controlLayout.setContentsMargins(5, 0, 5, 0)
        self.controlLayout.addWidget(self.playButton)

        self.lbl = QLineEdit('00:00:00')
        self.lbl.setReadOnly(True)
        self.lbl.setFixedWidth(70)
        self.lbl.setUpdatesEnabled(True)
        self.lbl.selectionChanged.connect(
            lambda: self.lbl.setSelection(0, 0))
        self.elbl = QLineEdit('00:00:00')
        self.elbl.setReadOnly(True)
        self.elbl.setFixedWidth(70)
        self.elbl.setUpdatesEnabled(True)
        self.elbl.selectionChanged.connect(
            lambda: self.elbl.setSelection(0, 0))
        self.positionSlider = QSlider(Qt.Orientation.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)
        self.positionSlider.setSingleStep(10)
        self.positionSlider.setPageStep(20)
        self.positionSlider.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.positionSlider.resize(self.positionSlider.sizeHint())
        self.controlLayout.addWidget(self.pauseButton)
        self.controlLayout.addWidget(self.stopButton)
        self.controlLayout.addWidget(self.volumeSlider)
        self.controlLayout.addWidget(self.positionSlider)
        self.controlLayout.addWidget(self.lbl)
        self.controlLayout.addWidget(self.elbl)

    def changeFile(self, file_path):

        self.file_path = file_path
        self.mediaPlayer.setSource(QUrl.fromLocalFile(self.file_path))
        self.playButton.setEnabled(False)
        self.stopButton.setEnabled(True)
        self.positionSlider.setValue(0)

    def stop(self):
        self.mediaPlayer.stop()
        self.mediaPlayer.setSource(QUrl.fromLocalFile(self.file_path))

    def play(self):
        self.mediaPlayer.play()

    def pause(self):
        self.mediaPlayer.pause()

    def setVolume(self, position):
        self.audioOutput.setVolume(position / 100)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def mediaStateChanged(self, state):
        if self.mediaPlayer.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.playButton.setEnabled(False)
            self.pauseButton.setEnabled(True)
            self.stopButton.setEnabled(True)
        else:
            self.playButton.setEnabled(True)
            self.pauseButton.setEnabled(False)
        if self.mediaPlayer.playbackState() == QMediaPlayer.PlaybackState.StoppedState:
            self.stopButton.setEnabled(False)
            self.mediaPlayer.setSource(
                QUrl.fromLocalFile(self.file_path))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)
        mtime = QTime(0, 0, 0, 0)
        mtime = mtime.addMSecs(self.mediaPlayer.position())
        self.lbl.setText(mtime.toString())
        if mtime == mtime.addMSecs(self.mediaPlayer.duration()):
            self.stop()
            self.playButton.setEnabled(True)
            self.pauseButton.setEnabled(False)
            self.stopButton.setEnabled(False)
            self.positionSlider.setValue(0)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)
        mtime = QTime(0, 0, 0, 0)
        mtime = mtime.addMSecs(self.mediaPlayer.duration())
        self.elbl.setText(mtime.toString())

    def handleError(self):
        self.playButton.setEnabled(False)
        print("Error: ", self.mediaPlayer.errorString())
