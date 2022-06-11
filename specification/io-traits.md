# Definition
An I/O Traits is a collection of I/O characteristics from different sources. It is a direct aggregated, so we specify the sources here and reference their documentation where available.
## Sources
The primary sources of I/O characteristics Luxio recognizes are a Flux jobspec, Darshan I/O trace, source code analysis, and binary analysis. The Flux jobspec is defined at https://flux-framework.readthedocs.io/projects/flux-rfc/en/latest/spec_14.html, and the Darshan input is defined at https://www.mcs.anl.gov/research/projects/darshan/docs/darshan-util.html . The Flux jobspec represents information about runtime, number of processes, location of binary and arguments, and user id. The Darshan trace has a large number of counters, including things such as POSIX opens, POSIX writes, stdio flushes, etc. For source code analysis, it very much depends on what kind of source code is being analyzed. Up to now, our lab has created a simple source code analyzer using the Clang AST (see https://libclang.readthedocs.io/en/latest/_modules/clang/cindex.html ) which can calculate total size written and read in the stdio or POSIX interfaces, as well as the number of operations, and estimate I/O time based on this. This is a simple tool and not provided here as of yet, because it needs more testing and improvement to function effectively across a wide variety of scenarios. Our lab has also done other I/O characterization based on source code and binary analysis in the Vidya paper (http://www.cs.iit.edu/~scs/assets/files/devarajan2018vidya_paper.pdf ), this was found to be too detailed to use in the Luxio environment currently, but provides some useful insight into the applications and limitations of source code analysis techniques.