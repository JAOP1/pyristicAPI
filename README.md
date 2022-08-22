# pyristicAPI
 Pyristic as a api service. This project is pretty helpful when you aren't
 a python developer and you would like to include pyristic in your proyect or
 you wanted use pyristic in your client.

 ## Dockerfile
 We suggest to you open the project using a docker container, so firstly you have to
 install docker, for more details about the installation click here: [docker install](https://docs.docker.com/get-docker/). Lets start!

 1. The project has a dockerfile in the root directory. You have to type the following to build the image, this image has everything needed to start the server.

```
docker build --rm -t pyristic-image .
```

2. Finally, if the image was successfully created, you can continue with the line that executes a container using the image with the name *pyristic-image*. The server will be listening in the port 80, so if you are running the container in a local machine you can see the interactive api typing in your web browser localhost:80/ 

```
docker run --rm -it -p 80:80 --name pyristic-container pyristic-image
```

3. If you would like mount your optimization problem, you can! The necessary is only include the folder path where is located your files. As follow:

```
docker run --rm -it -p 80:80 -v $(pwd)/LOCAL_PATH:/pyristic_api/app/optimization_problem --name pyristic-container pyristic-image
```

In the LOCAL_PATH, you replace by the path to you folder, where the python files required are. Is too important that the folder path has a '__init__.py' file.  The navigation until you local_path should be thinking in the current path where you executed the first command.

4. Optionally, you can open the container's console, it is very helpful when you want see if the files are copied well or make a debugging.

```
docker exec -it pyristic-container bash
```

