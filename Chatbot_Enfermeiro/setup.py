from setuptools import setup, find_packages

setup(
    name="Chatbot_Enfermeiro",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Flask>=2.0.0",
        "pytest>=6.0.0",
        "mypy>=0.910",
    ],
    entry_points={
        "console_scripts": [
            "chatbot-enfermeiro=run:app.run",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)