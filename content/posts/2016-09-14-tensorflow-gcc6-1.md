---
title: Compile TensorFlow from source with gcc6.1
tags: ['tensorflow', 'python']
status: published
summary: Where we build TensorFlow from scratch.
---


Due to two bugs in gcc 6.1
[affecting the re2 library](https://github.com/google/re2/issues/102)
(one of which has been fixed in 6.2)),
[TensorFlow](https://www.tensorflow.org/) cannot be
[compiled from source](https://www.tensorflow.org/versions/r0.10/get_started/os_setup.html)
one some systems (including my Debian Testing install).

To work around the issue, modify ``tensorflow/workspace.bzl`` and
change the re2 description to:

```
native.git_repository(
  name = "com_googlesource_code_re2",
  remote = "https://github.com/stefanv/re2.git",
  commit = "86503cb89d82b723ae0bce35e1e09524910cd319",
)
```

The re2 library is now downloaded from my fork, which applies a
[one line patch](https://github.com/stefanv/re2/commit/86503cb89d82b723ae0bce35e1e09524910cd319).

Compile the TensorFlow Python package as usual with:

```
bazel build -c opt //tensorflow/tools/pip_package:build_pip_package
bazel-bin/tensorflow/tools/pip_package/build_pip_package /tmp/tensorflow_pkg
```

After installing the pip wheel using

```
pip install /tmp/tensorflow_pkg/*.whl
```

you should have a working installation.  If importing fails with

```text
ImportError: cannot import name 'pywrap_tensorflow'
```

switch out of the TensorFlow source directory and try again.
