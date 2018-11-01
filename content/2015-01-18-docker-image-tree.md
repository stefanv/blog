Title: Visualizing and pruning the docker image tree
Date: 2015-01-18
Tags: docker
Status: published
Summary: Where we prune unused Docker images, and save a lot of disk space.

Visualizing the Docker image dependency tree is a useful way of
checking image sizes and inter-image dependencies.  Since images
occupy a lot of disk space, we may also want to prune unused images.

## Visualizing image dependencies

In version 1.2.0 of Docker, the image dependency tree is available via
the ``docker images --tree`` command:

```
$ docker images --tree
Warning: '--tree' is deprecated, it will be removed soon. See usage.
├─511136ea3c5a Virtual Size: 0 B
│ ├─5bc37dc2dfba Virtual Size: 192.5 MB
│ │ └─61cb619d86bc Virtual Size: 192.7 MB
│ │   └─3f45ca85fedc Virtual Size: 192.7 MB
│ │     └─78e82ee876a2 Virtual Size: 192.7 MB
│ │       └─dc07507cef42 Virtual Size: 192.7 MB
│ │         └─86ce37374f40 Virtual Size: 192.7 MB
│ │           └─d76983dc2ebd Virtual Size: 213.3 MB
│ │             └─04a01662a6a8 Virtual Size: 214.5 MB
│ │               └─7769c00dfefe Virtual Size: 525.9 MB
│ │                 └─6ac8d6e449b1 Virtual Size: 525.9 MB
│ │                   └─e3a84ca24205 Virtual Size: 525.9 MB
│ │                     └─26f10d07659d Virtual Size: 525.9 MB
│ ├─e12c576ad8a1 Virtual Size: 198.9 MB
│ │ └─102eb2a101b8 Virtual Size: 199.1 MB
│ │   └─530dbbae98a0 Virtual Size: 199.1 MB
│ │     └─37dde56c3a42 Virtual Size: 199.1 MB
│ │       └─8f118367086c Virtual Size: 228.5 MB
│ │         └─277eb4304907 Virtual Size: 228.5 MB Tags: ubuntu:utopic, ubuntu:14.10
...
```

However, the Docker team is trying to streamline its client, and has
scheduled this feature for deprecation.  How, then, do we replicate
its behavior?

Enter [DockerViz](https://github.com/justone/dockviz).  Grab a binary
from [gobuild.io](http://gobuild.io/github.com/justone/dockviz) and
place it somewhere on your path.

### Querying the Docker image status

The Docker server can be queried via its
[public API](https://docs.docker.com/reference/api/docker_remote_api/).
It is typically available either on ``http://localhost:4243`` or
``/var/run/docker.sock``.

One of the following two calls should therefore extract the image
status:

```
curl -s http://localhost:4243/images/json?all=1
echo -e "GET /images/json?all=1 HTTP/1.0\r\n" | nc -U /var/run/docker.sock
```

On my machine, the second query returns:

```
HTTP/1.0 200 OK
Content-Type: application/json
Date: Sun, 18 Jan 2015 17:41:34 GMT

[{"Created":1421528518,"Id":"d6244a9e8b5ff885579c8c7d203e4da703e3e80621449dbbd58c365dba5c83b1","ParentId":"b68521997660ae8a6916037696cf716ca415bba0766487bfa5b79cda4adfb62c","RepoTags":["datascience-base:latest"],"Size":0,"VirtualSize":2041562468}
,{"Created":1421528517,"Id":"b68521997660ae8a6916037696cf716ca415bba0766487bfa5b79cda4adfb62c","ParentId":"d3cb571e5e16fce16a59c16c87e01ea4051d7cae016dba90688c9e4a53a921c4","RepoTags":["\u003cnone\u003e:\u003cnone\u003e"],"Size":0,"VirtualSize":2041562468}
...
```

DockViz parses this JSON and outputs a formatted tree:

```
$ cat ~/scripts/docktree 
echo -e "GET /images/json?all=1 HTTP/1.0\r\n" | nc -U /var/run/docker.sock | tail -n +5 | dockviz images --tree
$ docktree
├─511136ea3c5a Virtual Size: 0.0 B
│ ├─5bc37dc2dfba Virtual Size: 192.5 MB
│ │ └─61cb619d86bc Virtual Size: 192.7 MB
│ │   └─3f45ca85fedc Virtual Size: 192.7 MB
│ │     └─78e82ee876a2 Virtual Size: 192.7 MB
│ │       └─dc07507cef42 Virtual Size: 192.7 MB
│ │         └─86ce37374f40 Virtual Size: 192.7 MB
│ │           └─d76983dc2ebd Virtual Size: 213.3 MB
│ │             └─04a01662a6a8 Virtual Size: 214.5 MB
│ │               └─7769c00dfefe Virtual Size: 525.9 MB
│ │                 └─6ac8d6e449b1 Virtual Size: 525.9 MB
│ │                   └─e3a84ca24205 Virtual Size: 525.9 MB
│ │                     └─26f10d07659d Virtual Size: 525.9 MB
│ ├─e12c576ad8a1 Virtual Size: 198.9 MB
│ │ └─102eb2a101b8 Virtual Size: 199.1 MB
│ │   └─530dbbae98a0 Virtual Size: 199.1 MB
│ │     └─37dde56c3a42 Virtual Size: 199.1 MB
│ │       └─8f118367086c Virtual Size: 228.5 MB
│ │         └─277eb4304907 Virtual Size: 228.5 MB Tags: ubuntu:14.10, ubuntu:utopic
```

Note that, on my system, the first branch of the tree is dangling,
i.e. not associated with a tagged image--I must have removed a tagged
image earlier, and these are its remaining dependencies.

## Pruning unusued images

Built and downloaded Docker images quickly gobble up a lot of space:

```
$ sudo du -hcs /var/lib/docker/
10G	/var/lib/docker/
10G	total
```

The ``docker images`` command allows us to
[list dangling images](https://docs.docker.com/reference/commandline/cli/#images):

```
docker images --filter dangling=true --quiet
```

And we obtain a list of containers (images that were fired up and
modified) using:

```
docker ps -aq
```

I remove both of these with the following script (WARNING: This
will delete ALL containers and any unused, downloaded images, so use
with caution!):

```
#!/bin/bash
CONTAINERS=$(docker ps -aq)
IMAGES=$(docker images --filter dangling=true --quiet)
if [[ $CONTAINERS ]]; then
    docker rm $CONTAINERS
else
    echo "No containers to remove"
fi

if [[ $IMAGES ]]; then
    docker rmi $IMAGES
else
    echo "No dangling images to remove"
fi
```

Then:

```
$ docker-clean
$ sudo du -hcs /var/lib/docker/
6.6G	/var/lib/docker/
6.6G	total
$ docktree
└─511136ea3c5a Virtual Size: 0.0 B
  ├─e12c576ad8a1 Virtual Size: 198.9 MB
  │ └─102eb2a101b8 Virtual Size: 199.1 MB
  │   └─530dbbae98a0 Virtual Size: 199.1 MB
  │     └─37dde56c3a42 Virtual Size: 199.1 MB
  │       └─8f118367086c Virtual Size: 228.5 MB
  │         └─277eb4304907 Virtual Size: 228.5 MB Tags: ubuntu:utopic, ubuntu:14.10
  ├─d497ad3926c8 Virtual Size: 192.5 MB
  │ └─ccb62158e970 Virtual Size: 192.7 MB
  │   └─e791be0477f2 Virtual Size: 192.7 MB
...
```

Note that, now, all branches of the tree are associated with tagged
images.  If I remove ``ubuntu:utopic``, I can again run the pruning
process to get rid of its left-over dependencies.
