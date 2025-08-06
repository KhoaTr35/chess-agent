from setuptools import setup, find_packages

setup(
    name="chess-agent-project",
    version="0.1.0",
    description="An interactive chess game with AI agent capabilities",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "python-chess>=1.999",
        "pygame>=2.1.0",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "chess-game=src.gui.chess_gui:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
