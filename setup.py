import os
import sys
import torch
from setuptools import setup
from torch.utils import cpp_extension

sources = ["src/mcp.cpp"]

# mcp_plugin_dir = os.path.dirname(os.path.abspath(__file__))
mcp_home = os.environ.get("MCP_HOME")
if mcp_home is None:
    print("MCP_HOME is not set.")
    sys.exit(1)

nccl_home = os.environ.get("NCCL_HOME")
if nccl_home is None:
    print("NCCL_HOME is not set.")
    sys.exit(1)

include_dirs = [f"{os.path.dirname(os.path.abspath(__file__))}/include/"]
include_dirs.append(f"{mcp_home}/include/")
# include_dirs.append(f"{nccl_home}/include/")

plugin_libraries = ["mscclpp"]
plugin_library_dirs = [f"{mcp_home}/lib/"]
# plugin_library_dirs.append(f"{nccl_home}/lib/")

if torch.cuda.is_available():
    module = cpp_extension.CUDAExtension(
        name="mcp_collectives",
        sources=sources,
        include_dirs=include_dirs,
        libraries=plugin_libraries,
        library_dirs=plugin_library_dirs,
    )
else:
    module = cpp_extension.CppExtension(
        name="mcp_collectives",
        sources=sources,
        include_dirs=include_dirs,
        libraries=plugin_libraries,
        library_dirs=plugin_library_dirs,
    )

setup(
    name="Mcp-Collectives",
    version="0.0.1",
    ext_modules=[module],
    cmdclass={'build_ext': cpp_extension.BuildExtension}
)
