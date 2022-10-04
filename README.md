[This is a work in progress.]

### Introduction

App URL: https://simplified-text.herokuapp.com/

Idea URL: https://docs.google.com/presentation/d/e/2PACX-1vSMrCTVihqxV4poGJ_k-HKpSnCewlI_5i2SxzOGo8LFR7gEQmfVqAMQCAQphr_XiKKXD8JkTi1f1iWa/pub?start=false&loop=false&delayms=10000


The app lets you enter the text you would like to simplify and has an interface that comprises a text area and submit button. On submitting, the simplified text is displayed.

![image](https://user-images.githubusercontent.com/89630232/193754702-17df0f18-befe-439b-b72a-5b9b3fba28ab.png)

The app has been created using the *Flask* framework of python and deployed via *heroku's container registry*.


### Creating and running the docker image on local machine

`docker build -t <name of the docker image>:<tag> .`

`docker run -d -p 5000:5000 <name of the docker image>:<tag>`

### Deploying the image on heroku

`heroku login`

`heroku container:login`

`docker tag <name of the docker image>:<tag> registry.heroku.com/<name of the app on heroku>/web`

`docker push registry.heroku.com/<name of the app on heroku>/web`

`heroku container:release web -a <name of the app on heroku>`









[Acknowledgement:

OpenAI's GPT-3 has been used to generate simplified version of the entered text. The app is solely for demonstration purpose and does not serve any commercial interest.]

