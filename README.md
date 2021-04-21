Everybody is wondering about 2020-2021 *Covid-19* pandemic and want to understand what is going on. It will help if you have some data in hand and have some easy ways to look into specific indicators you have in mind.

Some government organiztions publish limited sets of data as their data open initiatives. If you are new to data science and want to get a quick start, you can try with this project. By following the instructions, you will be able to run your own analysis in 15 minutes.

###Setup

1. Install Docker Desktop software from Docker.com to your workstation(Windows, Mac, Linux) 
2. Checkout and run prepared docker image from DockerHub to your workstation. It will set up and launch a local web server on your own workstation.

###Features

1. With a provided link, you will be able to access locally hosted Jupyter Notebooks web service, see sample analysis programs(with source code) for Ottawa and Toronto open data.
2. You can run data refresh daily to get latest number updates, like most of people do these days.
3. You will be able to work on your own Python programs, with raw data you downloaded from other sources.

###Usage

###### Download and run the docker image
`$ docker run --name optional_container_name -v vol01:/home/jovyan/vol_mount -p 2021:8888 -p 2020:5000 bigdata2020c/covid_data_probe`

Providing container name is optional. Assuming you have created a volume named "vol01" when installing Docker software.

###### Browse to following link on your workstation
[http://127.0.0.1:2020](http://127.0.0.1:2020)

###Note

Current sample datasets includes open data for Ottawa and Toronto. You can add data for your own city and work with your analysis algorithm or plotting. I might be able to help if you have particular requirements and suggestions.

Vesion: 1.0.0

##Contributors
bigdata2020c at GMAIL

- [project on GitHub](https://github.com/Ming-D-BigData/CovidDataProbe)
- [Images on Docker Hub](https://hub.docker.com/repository/docker/bigdata2020c/covid_data_probe)


