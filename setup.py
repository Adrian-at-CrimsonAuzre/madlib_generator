import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
        name="madlib_generator",
        version="0.1.1",
        author="Adrian-at-CrimsonAuzre",
        author_email="adrian@crimsonazure.com",
        description="A small example package",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/Adrian-at-CrimsonAuzre/madlib_generator",
        classifiers=[
                "Programming Language :: Python :: 3",
                "License :: OSI Approved :: MIT License",
                "Operating System :: OS Independent",
                ],
        package_dir={"": "src"},
        packages=setuptools.find_packages(where="src"),
        python_requires=">=3.6",
        include_package_data=True,
        package_data={'madlib': ['data/*.json.gz']},
        )
