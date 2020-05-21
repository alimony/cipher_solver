import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="cipher_solver",
    version="1.0.0",
    description="Algorithm for solving simple, monoalphabetic substitution ciphers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alimony/cipher_solver",
    author="Markus Amalthea Magnuson",
    author_email="markus@polyscopic.works",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Security :: Cryptography",
        "Topic :: Text Processing :: Linguistic",
    ],
    keywords="monoalphabetic-substitution-cipher substitution-cipher cipher",
    project_urls={
        "Documentation": "https://alimony.github.io/cipher_solver/",
        "Source": "https://github.com/alimony/cipher_solver",
        "Tracker": "https://github.com/alimony/cipher_solver/issues",
    },
    packages=["cipher_solver"],
    install_requires=["numpy"],
    python_requires=">=3.6",
    entry_points={"console_scripts": ["cipher_solver=cipher_solver.cli:main"]},
)
