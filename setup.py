import os

from setuptools import Extension, setup
from Cython.Build import cythonize

extra_compile_args = ["/O2" if os.name == "nt" else "-O3"]
define_macros = [('CYTHON_WITHOUT_ASSERTIONS', None)]

setup(
    name="models.types",
    ext_modules=cythonize(
        [
            Extension(
                "models.types",
                ["src/models/types.pyx"],
                define_macros=define_macros
            )
        ],
        compiler_directives={'language_level': "3"}
    ),
    package_dir={"": "src"}
)
